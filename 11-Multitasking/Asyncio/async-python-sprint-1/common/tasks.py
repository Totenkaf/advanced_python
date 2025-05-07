# Copyright (c) 2023 Artem Ustsov

import enum
from concurrent.futures import ThreadPoolExecutor
import csv
from itertools import chain
from multiprocessing import Manager, Process
from multiprocessing import Queue as mpQueue
from multiprocessing.dummy import Pool
from statistics import mean
from typing import Dict, List, Optional, Union
import threading
from queue import Queue

from common.base import QueueMixin
from external.client import YandexWeatherAPI
from external.analyzer import analyze_json
from common.log import get_logger
from utils import get_url_by_city_name

LOG = get_logger()


class DataFetchingTask(YandexWeatherAPI, QueueMixin):
    """Fetch data from YandexWeatherAPI"""

    def fetch_cities(self, cities: Union[List[str], str]) -> Queue:
        """Fetch data by url using ThreadPoolExecutor [I/O bound task] and put it into queue

        :param cities: List with city names
        :return: Shared queue
        """

        LOG.debug("DataFetchingTask::fetch_cities")

        with ThreadPoolExecutor() as pool:
            for city_name in cities:
                city_url = get_url_by_city_name(city_name)

                LOG.info("Start fetching weather data for %s by url=%s", city_name, city_url)
                self.queue = pool.submit(self.get_forecasting, city_url)

        return self.queue


class DataCalculationTask:
    """Calculate weather stats and set a comfortability rating"""

    def __init__(self):
        self.processes: list[Process] = []
        self.queue = Manager().Queue()

    def __run_processes(self) -> None:
        """Start created processes to execute CPU bound tasks

        :return: None
        """

        [proc.start() for proc in self.processes]
        LOG.debug(
            "DataCalculationTask::__run_processes: pid - name \n %s", [f"{i.pid}-{i.name}" for i in self.processes],
        )

    def __join_processes(self) -> None:
        """Complete created processes to execute CPU bound tasks

        :return:
        """

        [proc.join() for proc in self.processes]
        LOG.debug(
            "DataCalculationTask::__join_processes: pid - name \n %s", [f"{i.pid}-{i.name}" for i in self.processes],
        )

    @staticmethod
    def _calculate_common_avg_temperature(dates_info: List[Dict]) -> float:
        """Calculate common average temperate.
        Process in avg_temp is None or zero. If avg_temp is None - mean does not calculate

        :param dates_info: Dates info from YWApi
        :return: Common average temperate in city for all dates
        """

        LOG.debug("DataCalculationTask::_calculate_common_avg_temperature")
        common_avg_temperature = [daily_avg_temp for d in dates_info
                                  if (daily_avg_temp := d.get("temp_avg"))
                                  and isinstance(daily_avg_temp, (int, float))]
        return round(mean(iter(common_avg_temperature or [0])), 1)

    @staticmethod
    def _calculate_common_condition(dates_info: List[Dict]) -> float:
        """Calculate common average temperate.
        Process in relevant_cond_hours is None or zero. If relevant_cond_hours is None orequal to zero
        - mean does not calculate

        :param dates_info: Dates info from YWApi
        :return: Common condition in city for all dates
        """

        LOG.debug("DataCalculationTask::_calculate_common_condition")
        common_condition = [daily_cond for d in dates_info
                            if (daily_cond := d.get("relevant_cond_hours"))
                            and isinstance(daily_cond, int)]
        return round(mean(iter(common_condition or [0])), 1)

    @classmethod
    def calculate_cities_weather_info(cls, city_response: dict, queue: mpQueue) -> None:
        """Performs daily average temperature calculation using analyzer.py.
        Pre-aggregates information for further processing

        :param city_response: City response data object
        :param queue: Shared queue
        :return: None
        """

        LOG.debug("DataCalculationTask::calculate_cities_weather_info")
        if not city_response:
            LOG.warning("Empty city_response. Skipping")
            return

        city_info = {
            "name": city_response["geo_object"]["locality"]["name"],
            "dates_info": [*analyze_json(city_response).get("days")],
        }

        city_info.update(
            temp_avg=cls._calculate_common_avg_temperature(city_info["dates_info"]),
            cond_avg=cls._calculate_common_condition(city_info["dates_info"]),
        )

        LOG.debug("DataCalculationTask::format_response_info - %s", city_info)
        queue.put(city_info)

    @staticmethod
    def calculate_cities_rating(cities_stats: List[Dict]) -> List[Dict]:
        """Calculate a city rating according to common average temperature and condition hours

        :param cities_stats: Precalculated cities stats as list
        :return: Ready statistics by cities for further aggregation
        """

        LOG.debug("DataCalculationTask::calculate_cities_rating")
        result = sorted(cities_stats, key=lambda k: (-k["temp_avg"], -k["cond_avg"]))
        for i, value in enumerate(result):
            value["rating"] = i + 1

        return result

    def calculate_cities_stats(self, queue: Queue) -> List[Dict]:
        """Make a cities statistic calculation

        :param queue: Shared queue
        :return: Ready statistics by cities for further aggregation
        """

        LOG.debug("DataCalculationTask::calculate_cities_stats")
        for _ in range(queue.qsize()):
            self.processes.append(
                Process(
                    target=self.calculate_cities_weather_info,
                    args=(queue.get().result(), self.queue),
                )
            )
        self.__run_processes()
        self.__join_processes()

        cities_stats = []
        while not self.queue.empty():
            cities_stats.append(self.queue.get())

        return self.calculate_cities_rating(cities_stats)


class DataAggregationTask(YandexWeatherAPI):
    """Aggregate stats with user-friendly format and save it to cities_stats.csv [I/O bound task]"""

    class CSVFields(str, enum.Enum):
        """Enum for friendly commons"""

        CITY = "Город/День"
        AVERAGE = "Среднее"
        RATING = "Рейтинг"
        EMPTY = ""
        TEMP_AVERAGE = "Температура, среднее"
        CONDITION_AVERAGE = "Без осадков, среднее"

    def __init__(self) -> None:
        self.csv_locking = threading.Lock()
        self.writer: Optional[csv.DictWriter] = None

    def __create_base_fields(self, city_result: dict) -> list:
        """Make a table headers

        :param city_result: Specific city stats
        :return: List with future table headers
        """

        LOG.debug("DataAggregationTask::__create_base_fields")
        return [
            self.CSVFields.CITY.value,
            self.CSVFields.EMPTY.value,
            *chain(i["date"] for i in city_result["dates_info"]),
            self.CSVFields.AVERAGE.value,
            self.CSVFields.RATING.value,
        ]

    def __save_csv(self, city) -> None:
        """Download an info with city stats as a .csv file

        :param city: Specific city
        :return: None
        """

        LOG.debug("DataAggregationTask::__save_csv")
        row_temp = {
            self.CSVFields.CITY.value: city["name"],
            self.CSVFields.EMPTY.value: self.CSVFields.TEMP_AVERAGE.value,
            self.CSVFields.AVERAGE.value: city["temp_avg"],
            self.CSVFields.RATING.value: city["rating"],
        }

        row_cond = {
            self.CSVFields.CITY.value: self.CSVFields.EMPTY.value,
            self.CSVFields.EMPTY.value: self.CSVFields.CONDITION_AVERAGE.value,
            self.CSVFields.AVERAGE.value: city["cond_avg"],
            self.CSVFields.RATING.value: self.CSVFields.EMPTY.value,
        }

        for date in city["dates_info"]:
            row_temp[date["date"]] = date["temp_avg"]
            row_cond[date["date"]] = date["relevant_cond_hours"]

        self.writer.writerows([row_temp, row_cond])
        LOG.info("DataAggregationTask::__save_csv::written - %s", city["name"])

    def aggregate_result(self, result: List[Dict]) -> None:
        """Make a general aggregation

        :param result: Ready statistics by cities
        :return: None
        """

        LOG.debug("DataAggregationTask::aggregate_result")
        with open("cities_stats.csv", "w", newline="", encoding='utf-8') as file:
            self.writer = csv.DictWriter(file, fieldnames=self.__create_base_fields(result[0]))
            self.writer.writeheader()

            LOG.info("DataAggregationTask::aggregate_result::writeheader")
            with ThreadPoolExecutor() as pool:
                pool.map(self.__save_csv, result)


class DataAnalyzingTask(YandexWeatherAPI):
    """Make a verdict what cities are most comfortable for living in [CPU bound task]"""

    max_temp: int = 0
    max_cond: int = 0
    max_city_name: str = str()

    def __init__(self, result: List[Dict]) -> None:
        self.result = result
        self.__set_max_temp_cond()

    def __set_max_temp_cond(self) -> None:
        """Find a city with the highest average temp and average conditions for all dates

        :return: None
        """

        LOG.debug("DataAnalyzingTask::__set_max_temp_cond")
        max_city = next(iter(self.result), None)

        self.__class__.max_temp = max_city["temp_avg"]
        self.__class__.max_cond = max_city["cond_avg"]
        self.__class__.max_city_name = max_city["name"]

    @classmethod
    def checking_max_cities(cls, result: dict) -> Optional[str]:
        """Check if given city has the highest average temp and average conditions for all dates
        and return its name

        :param result: Ready statistics by cities
        :return: None
        """

        LOG.debug("DataAnalyzingTask::checking_max_cities")
        if result["temp_avg"] == cls.max_temp and result["cond_avg"] == cls.max_cond:
            return result["name"]

    def analyze_result(self) -> List[str]:
        """Make the main verdict on favorable cities

        :return: List with the most comfortable cities to living in

        """

        LOG.info("DataAnalyzingTask::analyze_result")
        with Pool(processes=4) as pool:
            result = pool.map(DataAnalyzingTask.checking_max_cities, self.result)
        return [city for city in result if city is not None]

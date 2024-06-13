# Copyright (c) 2023 Artem Ustsov

from common.log import get_logger
from common.tasks import DataFetchingTask
from common.tasks import DataCalculationTask
from common.tasks import DataAggregationTask
from common.tasks import DataAnalyzingTask
from utils import CITIES

LOG = get_logger()


def main() -> None:
    """Run pipeline to get comfortable cities for living in:
    [1] Fetch data from YandexWeatherAPI
    [2] Calculate weather stats and set a comfortability rating
    [3] Aggregate stats with user-friendly format and save it to cities_stats.csv
    [4] Make a verdict what cities are most comfortable for living in

    :return: None
    """

    queue = DataFetchingTask().fetch_cities(list(CITIES.keys()))
    result = DataCalculationTask().calculate_cities_stats(queue)
    DataAggregationTask().aggregate_result(result)
    good_cities = DataAnalyzingTask(result).analyze_result()

    print(f"The most comfortable cities to living in: {', '.join(map(str, good_cities))}")


if __name__ == "__main__":
    main()

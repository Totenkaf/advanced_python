# Copyright (c) 2023 Artem Ustsov

import pytest
from queue import Queue
from typing import Dict, List

from common.tasks import DataAggregationTask
from common.tasks import DataAnalyzingTask
from common.tasks import DataCalculationTask
from common.tasks import DataFetchingTask
from utils import CITIES


@pytest.fixture
def get_fetching_queue() -> Queue:
    return DataFetchingTask().fetch_cities(CITIES)


@pytest.fixture
def calculate_result() -> List[Dict]:
    return DataCalculationTask().calculate_cities_stats(DataFetchingTask().fetch_cities(CITIES))


@pytest.fixture
def make_csv() -> None:
    return DataAggregationTask().aggregate_result(
        DataCalculationTask().calculate_cities_stats(DataFetchingTask().fetch_cities(CITIES))
    )


@pytest.fixture
def full_pipeline_result() -> List[str]:
    return DataAnalyzingTask(
        DataCalculationTask().calculate_cities_stats(DataFetchingTask().fetch_cities(CITIES))
    ).analyze_result()

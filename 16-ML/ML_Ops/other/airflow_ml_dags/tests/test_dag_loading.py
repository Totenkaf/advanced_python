import pytest

from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def test_generate_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id='generate_data')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 1


def test_train_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id='train')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 6


def test_predict_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id='predict')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 3
    print(dag.task_dict)

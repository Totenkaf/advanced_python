import pytest

from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def assert_dag_dict_equal(source, dag):
    assert dag.task_dict.keys() == source.keys()
    for task_id, downstream_list in source.items():
        assert dag.has_task(task_id)
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream_list)


def test_generate_dag_structure(dagbag):
    dag = dagbag.get_dag(dag_id='generate_data')
    assert_dag_dict_equal(
        {
            'docker-airflow-generate-data': []
        },
        dag,
    )


def test_train_dag_structure(dagbag):
    dag = dagbag.get_dag(dag_id='train')
    assert_dag_dict_equal(
        {
            'wait-for-data': ['docker-airflow-preprocess'],
            'wait-for-target': ['docker-airflow-preprocess'],
            'docker-airflow-preprocess': ['docker-airflow-split'],
            'docker-airflow-split': ['docker-airflow-train'],
            'docker-airflow-train': ['docker-airflow-validate'],
            'docker-airflow-validate': []
        },
        dag,
    )


def test_predict_dag_structure(dagbag):
    dag = dagbag.get_dag(dag_id='predict')
    assert_dag_dict_equal(
        {
            'wait-for-predict-data': ['docker-airflow-predict_preprocess'],
            'docker-airflow-predict_preprocess': ['docker-airflow-predict'],
            'docker-airflow-predict': [],
        },
        dag,
    )

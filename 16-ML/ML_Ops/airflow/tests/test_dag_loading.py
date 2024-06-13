"""Copyright 2022 by Artem Ustsov"""


def test_generate_dag(dag_bag_fixture):
    dag = dag_bag_fixture.get_dag(dag_id="generate_data")

    assert dag is not None and dag_bag_fixture.import_errors == {}
    assert len(dag.tasks) == 1


def test_train_dag(dag_bag_fixture):
    dag = dag_bag_fixture.get_dag(dag_id="train")

    assert dag is not None and dag_bag_fixture.import_errors == {}
    assert len(dag.tasks) == 6


def test_predict_dag(dag_bag_fixture):
    dag = dag_bag_fixture.get_dag(dag_id="predict")

    assert dag is not None and dag_bag_fixture.import_errors == {}
    assert len(dag.tasks) == 3

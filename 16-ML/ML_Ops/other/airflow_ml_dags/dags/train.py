from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.python import PythonSensor
from docker.types import Mount
from utils import LOCAL_DATA_DIR, LOCAL_MLRUNS_DIR, default_args, wait_for_file


with DAG(
    'train',
    default_args=default_args,
    schedule_interval='@weekly',
    start_date=datetime(2022, 11, 1)
) as dag:
    wait_data = PythonSensor(
        task_id='wait-for-data',
        python_callable=wait_for_file,
        op_args=['/opt/airflow/data/raw/{{ ds }}/data.csv'],
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke"
    )

    wait_target = PythonSensor(
        task_id='wait-for-target',
        python_callable=wait_for_file,
        op_args=['/opt/airflow/data/raw/{{ ds }}/target.csv'],
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke"
    )

    preprocess = DockerOperator(
        image='airflow-preprocess',
        command='--input-dir /data/raw/{{ ds }} --output-dir /data/processed/{{ ds }}',
        network_mode='bridge',
        task_id='docker-airflow-preprocess',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=LOCAL_DATA_DIR, target='/data', type='bind')]
    )

    split = DockerOperator(
        image='airflow-split',
        command='--input-dir /data/processed/{{ ds }} --output-dir /data/splitted/{{ ds }}',
        network_mode='bridge',
        task_id='docker-airflow-split',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=LOCAL_DATA_DIR, target='/data', type='bind')]
    )

    train = DockerOperator(
        image='airflow-train',
        command='--input-dir /data/splitted/{{ ds }} --output-dir /data/models/{{ ds }}',
        network_mode='host',
        task_id='docker-airflow-train',
        do_xcom_push=True,
        auto_remove=True,
        mounts=[Mount(source=LOCAL_DATA_DIR, target='/data', type='bind'),
                Mount(source=LOCAL_MLRUNS_DIR, target='/mlruns', type='bind')],
    )

    validate = DockerOperator(
        image='airflow-validate',
        command='--input-dir /data/splitted/{{ ds }} --model-dir /data/models/{{ ds }} --output-dir /data/metrics/{{ ds }}',
        network_mode='host',
        task_id='docker-airflow-validate',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=LOCAL_DATA_DIR, target='/data', type='bind'),
                Mount(source=LOCAL_MLRUNS_DIR, target='/mlruns', type='bind')]
    )

    [wait_data, wait_target] >> preprocess >> split >> train >> validate

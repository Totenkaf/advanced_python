from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from utils import LOCAL_DATA_DIR, default_args


with DAG(
    'generate_data',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2022, 11, 1)
) as dag:
    generate = DockerOperator(
        image='airflow-generate-data',
        command='--output-dir /data/raw/{{ ds }}',
        network_mode='bridge',
        task_id='docker-airflow-generate-data',
        do_xcom_push=False,
        auto_remove=True,
        mounts=[Mount(source=LOCAL_DATA_DIR, target='/data', type='bind')]
    )

    generate

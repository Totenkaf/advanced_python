import os
from datetime import timedelta

from airflow.models import Variable
from airflow.utils.email import send_email_smtp


LOCAL_DATA_DIR = Variable.get('local_data_dir')
LOCAL_MLRUNS_DIR = Variable.get('local_mlruns_dir')


def wait_for_file(file_name):
    return os.path.exists(file_name)


def failure_callback(context):
    dag_run = context.get('dag_run')
    subject = f'DAG {dag_run} has failed'
    send_email_smtp(to=default_args['email'], subject=subject)


default_args = {
    'owner': 'liza_avsyannik',
    'email': ['liza.avsyannik@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': failure_callback
}

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_data():
    os.system('python /scripts/consumirAPI.py')

with DAG(
    'brewery_data_pipeline',
    default_args=default_args,
    description='Pipeline de dados de cervejarias',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
    )

    fetch_data_task

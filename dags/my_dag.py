from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from extract import get_exchange_rate_for_EUR


default_args = {
    'owner': 'PKotecka',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG("my_first_dag", start_date=datetime(2023, 2, 3), default_args=default_args,
         schedule_interval='@daily', catchup=False) as dag:
    task1 = PythonOperator(
        task_id='EUR_exchange_rate',
        python_callable=get_exchange_rate_for_EUR
    )
    task1

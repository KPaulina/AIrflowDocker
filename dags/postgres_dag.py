
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow import DAG
import os

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")

default_args = {
    'owner': 'PKotecka',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(dag_id='create_table',
         start_date=datetime(2023, 2, 5),
         schedule='@once',
         default_args=default_args,
         catchup=False) as dag:
    create_exchange_rate_table = PostgresOperator(
        task_id='create_exchange_rate_table',
        postgres_conn_id='postgres_localhost',
        sql = """
            CREATE TABLE IF NOT EXISTS public.exchange_rate (
            id serial PRIMARY KEY not null,
            main_currency_code varchar(10),
            currency_code varchar(10),
            time_last_update_utc varchar(50),
            rates numeric,
            timestamp timestamp default current_timestamp)
        """
    )
    create_exchange_rate_table

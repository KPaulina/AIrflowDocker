from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from consts import DATA_DIR, DATE, currency_list
from airflow.decorators import dag, task
import requests
import json
import os
import pandas as pd

default_args = {
    'owner': 'PKotecka',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id="etl_exchange_rate_dag", start_date=datetime(2023, 2, 3),
     default_args=default_args, schedule_interval='@daily')
def get_data_from_API_etl():

    @task()
    def get_exchange_rate():
        for currency in currency_list:
            url = f"https://open.er-api.com/v6/latest/{currency}"
            res = requests.request ('GET', url)
            json_data = res.json ()

            try:
                res.raise_for_status ()
            except requests.exceptions.HTTPError as e:
                print("Error: " + str (e))
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)

            with open(os.path.join(DATA_DIR, f'exchange_rate_{DATE}_{currency}.json'), 'w',
                       encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        return True


    @task()
    def json_to_dataframe(bool_value: bool):
        if bool_value:
            dfs = []
            for currency in currency_list:
                df_exchange_rate = pd.read_json(os.path.join(DATA_DIR, f'exchange_rate_{DATE}_{currency}.json'))
                df_exchange_rate = df_exchange_rate.reset_index()
                df_exchange_rate['main_currency_code'] = currency
                df_exchange_rate = df_exchange_rate.rename(columns={'index': 'currency_code'})
                df_exchange_rate = df_exchange_rate[['main_currency_code', 'currency_code', 'provider', 'time_last_update_utc', 'rates']]
                dfs.append (df_exchange_rate)
            df_exchange_rate = pd.concat(dfs)
            df_exchange_rate = df_exchange_rate.reset_index()
            return df_exchange_rate.to_json()

    @task()
    def load(df_exchange_rate):
        df_exchange_rate = pd.read_json(df_exchange_rate)
        df_exchange_rate = df_exchange_rate[['main_currency_code', 'currency_code', 'provider', 'time_last_update_utc', 'rates']]
        try:
            db = create_engine(f'postgresql+psycopg2://airflow:airflow@postgres/exchange_rate')
            conn = db.connect()
            df_exchange_rate.to_sql('exchange_rate', conn, schema='public', if_exists='append', index=False)
        except OperationalError as error:
            print(f'Operational error: {error}')


    bool_value = get_exchange_rate()
    df_exchange_rate = json_to_dataframe(bool_value)
    load(df_exchange_rate)


etl_exchange_rate_dag = get_data_from_API_etl()





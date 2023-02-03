import os
from consts import DATA_DIR, DATE
import requests
import json


def get_exchange_rate_for_EUR():
    url = f"https://open.er-api.com/v6/latest/EUR"
    res = requests.request('GET', url)
    json_data = res.json()

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    with open(os.path.join(DATA_DIR, f'exchange_rate_{DATE}.json'), 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

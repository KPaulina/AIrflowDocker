from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATE = str(datetime.now())[:10]
currency_list = ['USD', 'NOK', 'EUR', 'DKK', 'SEK']
#database connection
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = str(os.getenv('POSTGRES_PORT'))



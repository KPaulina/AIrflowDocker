from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATE = str(datetime.now())[:10]

import os
from dotenv import load_dotenv


load_dotenv()

ES_HOST = os.getenv("ES_HOST")
ES_USERNAME = os.getenv("ES_USERNAME", "elastic")
ES_PASSWORD = os.getenv("ES_PASSWORD")
ES_INDEX_NAME = os.getenv("ES_INDEX_NAME")
DATA_PATH = os.getenv("DATA_PATH")


marks_mapping = ["Процессор", "Камера", "Цена"]

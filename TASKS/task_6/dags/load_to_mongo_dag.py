from datetime import datetime

import pandas as pd
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task

TIKTOK_CSV_PATH = '../../resources/csv/tiktok_google_play_reviews.csv'

from TASKS.task_6.handlers.mongo_handler import MongoHandler

FILEPATH = ''


@dag(
    dag_id="load_data_to_mongo",
    start_date=datetime(2024, 1, 1),
    schedule="@once",
    catchup=False,
)
def load_to_mongo_dag():

    wait_for_file = FileSensor(
        task_id="wait_for_file", filepath=FILEPATH, poke_interval=5, timeout=60 * 5, mode="poke"
    )

    @task
    def load_data_to_mongo():
        handler = MongoHandler(db_name='tiktok')
        dataset = pd.read_csv(TIKTOK_CSV_PATH)


load_to_mongo_dag()

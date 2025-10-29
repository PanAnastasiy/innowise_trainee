import os

from dotenv import load_dotenv

from TASKS.task_5.spark_handler import SparkHandler

load_dotenv()

db_url = os.getenv('DB_PAGILA_URL')
db_properties = {
    "user": os.getenv('PG_USER'),
    "password": os.getenv('PG_PASSWORD'),
    "driver": "org.postgresql.Driver",
}

handler = SparkHandler(os.getenv('DB_PAGILA_URL'), db_properties)

employees_df = handler.get_data_from_table("actor")
print(employees_df.head())

import os

from dotenv import load_dotenv
from pyspark.sql.functions import count, desc

from TASKS.task_5.spark_handler import SparkHandler

load_dotenv()

db_properties = {
    "user": os.getenv('PG_USER'),
    "password": os.getenv('PG_PASSWORD'),
    "driver": "org.postgresql.Driver",
}

# путь к PostgreSQL драйверу
pg_jar = r"C:\Users\user\AppData\Roaming\JetBrains\DataGrip2025.2\jdbc-drivers\PostgreSQL\42.7.3\org\postgresql\postgresql\42.7.3\postgresql-42.7.3.jar"

# передаём jars в SparkHandler
handler = SparkHandler(os.getenv('DB_PAGILA_URL'), db_properties, jars=pg_jar)

film = handler.get_data_from_table('film')
category = handler.get_data_from_table('category')
film_category = handler.get_data_from_table('film_category')
actor = handler.get_data_from_table('actor')
film_actor = handler.get_data_from_table('film_actor')
rental = handler.get_data_from_table('rental')
inventory = handler.get_data_from_table('inventory')
payment = handler.get_data_from_table('payment')
customer = handler.get_data_from_table('customer')
address = handler.get_data_from_table('address')
city = handler.get_data_from_table('city')


df1 = (
    film_category.join(category, "category_id")
    .groupBy.agg(count("film_id").alias("num_movies"))
    .orderBy(desc("num_movies"))
)

df1.show()

import os
from typing import Any, Callable

from dotenv import load_dotenv
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import concat, count, dense_rank, desc, lit
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.functions import unix_timestamp, when

from TASKS.task_5.handlers.spark_handler import SparkHandler
from TASKS.utils.design import Color, Message

load_dotenv()

db_properties = {
    "user": os.getenv('PG_USER'),
    "password": os.getenv('PG_PASSWORD'),
    "driver": "org.postgresql.Driver",
}

pg_jar = "jars/postgresql-42.7.3.jar"


def spark_task(title: str) -> Callable[[Callable[..., DataFrame]], Callable[..., None]]:
    """
    Декоратор для обёртки задач Spark.
    Выводит заголовок, выполняет функцию и показывает результат с помощью df.show().
    """

    def decorator(func: Callable[..., DataFrame]) -> Callable[..., None]:
        def wrapper(self, *args: Any, **kwargs: Any) -> None:
            Message.print_message(title, Color.YELLOW, Color.LIGHT_WHITE)
            Message.print_message('Чуть-чуть подожди...', Color.CYAN, Color.LIGHT_WHITE)

            df: DataFrame = func(self, *args, **kwargs)

            if df is not None:
                df.show(truncate=False)

            Message.wait_for_enter()

        return wrapper

    return decorator


class Solution:
    """
    Класс для решения аналитических задач на основе базы данных Pagila с использованием PySpark.
    """

    def __init__(self) -> None:
        handler = SparkHandler(os.getenv('DB_PAGILA_URL'), db_properties, jars=pg_jar)
        self.film: DataFrame = handler.get_data_from_table('film')
        self.category: DataFrame = handler.get_data_from_table('category')
        self.film_category: DataFrame = handler.get_data_from_table('film_category')
        self.actor: DataFrame = handler.get_data_from_table('actor')
        self.film_actor: DataFrame = handler.get_data_from_table('film_actor')
        self.rental: DataFrame = handler.get_data_from_table('rental')
        self.inventory: DataFrame = handler.get_data_from_table('inventory')
        self.payment: DataFrame = handler.get_data_from_table('payment')
        self.customer: DataFrame = handler.get_data_from_table('customer')
        self.address: DataFrame = handler.get_data_from_table('address')
        self.city: DataFrame = handler.get_data_from_table('city')

    @spark_task("Количество фильмов каждой категории:")
    def task_1(self) -> DataFrame:
        """Возвращает количество фильмов в каждой категории, упорядоченных по убыванию."""
        return (
            self.film_category.join(self.category, "category_id")
            .groupBy("name")
            .agg(count("film_id").alias("num_movies"))
            .orderBy(desc("num_movies"))
        )

    @spark_task("Самые популярные актёры:")
    def task_2(self) -> DataFrame:
        """Возвращает топ-10 актёров по количеству прокатов фильмов."""
        return (
            self.actor.join(self.film_actor, "actor_id", "left")
            .join(self.inventory, "film_id", "left")
            .join(self.rental, "inventory_id", "left")
            .groupBy(
                concat(self.actor.last_name, lit(" "), self.actor.first_name).alias("actor_name")
            )
            .agg(count("rental_id").alias("total_rentals"))
            .orderBy(desc("total_rentals"))
            .limit(10)
        )

    @spark_task("Самые прибыльные категории:")
    def task_3(self) -> DataFrame:
        """Возвращает категорию с наибольшей суммой дохода по платежам."""
        return (
            self.category.join(self.film_category, "category_id", "left")
            .join(self.inventory, "film_id", "left")
            .join(self.rental, "inventory_id", "left")
            .join(self.payment, "rental_id", "left")
            .groupBy("name")
            .agg(spark_sum("amount").alias("revenue"))
            .orderBy(desc("revenue"))
            .limit(1)
        )

    @spark_task("Фильмы, которые пока что не в прокате:")
    def task_4(self) -> DataFrame:
        """Возвращает список фильмов, для которых нет записей в инвентаре."""
        return (
            self.film.join(self.inventory, "film_id", "left")
            .filter(self.inventory.inventory_id.isNull())
            .select("title")
            .orderBy("title")
        )

    @spark_task("Топ 3 актёров в категории фильмов <Дети>:")
    def task_5(self) -> DataFrame:
        """Возвращает топ-3 актёров по количеству фильмов в категории 'Children'."""
        df = (
            self.actor.join(self.film_actor, "actor_id")
            .join(self.film_category, "film_id")
            .join(self.category, "category_id")
            .filter(self.category.name == "Children")
            .groupBy(
                concat(self.actor.last_name, lit(" "), self.actor.first_name).alias("actor_name")
            )
            .agg(count("*").alias("film_count"))
        )

        w = Window.orderBy(desc("film_count"))
        return (
            df.withColumn("rank", dense_rank().over(w))
            .filter("rank <= 3")
            .orderBy(desc("film_count"))
        )

    @spark_task("Активность гостей по городам:")
    def task_6(self) -> DataFrame:
        """Возвращает количество активных и неактивных клиентов по городам."""
        return (
            self.customer.join(self.address, "address_id")
            .join(self.city, "city_id")
            .groupBy("city")
            .agg(
                spark_sum(when(self.customer.active == 1, 1).otherwise(0)).alias(
                    "active_customers"
                ),
                spark_sum(when(self.customer.active == 0, 1).otherwise(0)).alias(
                    "inactive_customers"
                ),
            )
            .orderBy(desc("inactive_customers"))
        )

    @spark_task("Лучшие категории по просмотрам, включающие заданные символы:")
    def task_7(self) -> DataFrame:
        """
        Возвращает лучшие категории фильмов по суммарному времени просмотров,
        разделяя их по городам, начинающимся с 'A' и содержащим '-'.
        """
        intermediate = (
            self.category.join(self.film_category, "category_id")
            .join(self.inventory, "film_id")
            .join(self.rental, "inventory_id")
            .join(self.customer, "customer_id")
            .join(self.address, "address_id")
            .join(self.city, "city_id")
            .withColumn(
                "hours", (unix_timestamp("return_date") - unix_timestamp("rental_date")) / 3600
            )
        )
        return intermediate

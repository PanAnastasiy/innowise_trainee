import threading

import pandas as pd
from pyspark.sql import SparkSession

from TASKS.utils.design import Color, Message


# Паттерн Singleton
class SparkLocalConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, jars: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_spark(jars)
        return cls._instance

    def _init_spark(self, jars: str = None):
        local_ip = "127.0.0.1"
        builder = (
            SparkSession.builder.appName("LocalConnection")
            .master("local[*]")
            .config("spark.driver.bindAddress", local_ip)
            .config("spark.driver.host", local_ip)
            .config("spark.network.timeout", "600s")
            .config("spark.locality.wait", "0s")
            .config("spark.driver.extraJavaOptions", "-Dlog4j2.configurationFile=log4j2.properties")
            .config("spark.hadoop.io.native.lib.available", "false")
        )

        if jars:
            builder = builder.config("spark.jars", jars)  # подключаем нужный драйвер

        self.spark = builder.getOrCreate()
        Message.print_message('Spark успешно проинициализирован!', Color.GREEN, Color.LIGHT_WHITE)
        Message.print_message(
            f'Версия Spark: {self.spark.version}', Color.PURPLE, Color.LIGHT_WHITE
        )

    def get_session(self):
        return self.spark


class SparkHandler:
    def __init__(self, db_url: str, db_properties: dict, jars: str = None):
        self.db_url = db_url
        self.db_properties = db_properties
        self.spark = SparkLocalConnection(jars).get_session()
        Message.print_message('SparkHandler инициализирован!', Color.GREEN, Color.LIGHT_WHITE)

    def get_data_from_table(self, table_name: str) -> pd.DataFrame:
        """Чтение таблицы из PostgreSQL в Pandas через Spark"""
        try:
            df_spark = self.spark.read.jdbc(
                url=self.db_url, table=table_name, properties=self.db_properties
            )
            Message.print_message(
                f'Данные из таблицы "{table_name}" успешно загружены в Spark!',
                Color.PURPLE,
                Color.LIGHT_WHITE,
            )
            # Преобразуем Spark DataFrame в Pandas DataFrame
            return df_spark
        except Exception as e:
            Message.print_message(
                f'Ошибка при загрузке таблицы "{table_name}": {e}', Color.RED, Color.LIGHT_WHITE
            )
            return None

    def execute_query(self, query: str) -> pd.DataFrame:
        """Выполнение произвольного SQL запроса через Spark"""
        try:
            df_spark = (
                self.spark.read.format("jdbc")
                .option("url", self.db_url)
                .option("dbtable", f"({query}) as subquery")
                .option("user", self.db_properties["user"])
                .option("password", self.db_properties["password"])
                .option("driver", self.db_properties["driver"])
                .load()
            )
            Message.print_message('SQL-запрос выполнен успешно!', Color.GREEN, Color.LIGHT_WHITE)
            return df_spark.toPandas()
        except Exception as e:
            Message.print_message(
                f'Ошибка выполнения SQL-запроса: {e}', Color.RED, Color.LIGHT_WHITE
            )
            return pd.DataFrame()

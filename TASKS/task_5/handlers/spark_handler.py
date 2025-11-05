import threading
from typing import Dict, Optional

import pandas as pd
from pyspark.sql import SparkSession

from TASKS.utils.design import Color, Message


class SparkLocalConnection:
    """
    Singleton-класс для локального подключения к Spark.
    """

    _instance: Optional["SparkLocalConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, jars: Optional[str] = None) -> "SparkLocalConnection":
        """
        Создает или возвращает единственный экземпляр класса.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_spark(jars)
        return cls._instance

    def _init_spark(self, jars: Optional[str] = None) -> None:
        """
        Инициализация SparkSession с локальными настройками.
        """
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
            builder = builder.config("spark.jars", jars)

        self.spark: SparkSession = builder.getOrCreate()
        Message.print_message('Spark успешно проинициализирован!', Color.GREEN, Color.LIGHT_WHITE)
        Message.print_message(
            f'Версия Spark: {self.spark.version}', Color.PURPLE, Color.LIGHT_WHITE
        )

    def get_session(self) -> SparkSession:
        """
        Получить экземпляр SparkSession.
        """
        return self.spark


class SparkHandler:
    """
    Класс для работы с данными через Spark.

    Attributes:
        db_url (str): URL подключения к базе данных.
        db_properties (dict): Словарь с параметрами подключения (user, password, driver).
        spark (SparkSession): Экземпляр SparkSession.
    """

    def __init__(
        self, db_url: str, db_properties: Dict[str, str], jars: Optional[str] = None
    ) -> None:
        """
        Инициализация SparkHandler.
        """
        self.db_url: str = db_url
        self.db_properties: Dict[str, str] = db_properties
        self.spark: SparkSession = SparkLocalConnection(jars).get_session()
        Message.print_message('SparkHandler инициализирован!', Color.GREEN, Color.LIGHT_WHITE)

    def get_data_from_table(self, table_name: str) -> Optional[pd.DataFrame]:
        """
        Загружает данные из таблицы базы данных в Spark DataFrame.
        """
        try:
            df_spark = self.spark.read.jdbc(
                url=self.db_url, table=table_name, properties=self.db_properties
            )
            Message.print_message(
                f'Данные из таблицы "{table_name}" успешно загружены в Spark!',
                Color.PURPLE,
                Color.LIGHT_WHITE,
            )
            return df_spark
        except Exception as e:
            Message.print_message(
                f'Ошибка при загрузке таблицы "{table_name}": {e}', Color.RED, Color.LIGHT_WHITE
            )
            return None

    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """
        Выполняет SQL-запрос через Spark и возвращает результат.
        """
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
            return df_spark
        except Exception as e:
            Message.print_message(
                f'Ошибка выполнения SQL-запроса: {e}', Color.RED, Color.LIGHT_WHITE
            )
            return None

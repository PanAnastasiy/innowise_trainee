from typing import Dict

import pytest

from TASKS.task_5.handlers.spark_handler import SparkHandler

# Заглушка параметров БД для теста
DB_URL = "jdbc:postgresql://localhost:5432/testdb"
DB_PROPERTIES: Dict[str, str] = {
    "user": "test_user",
    "password": "test_password",
    "driver": "org.postgresql.Driver",
}


@pytest.fixture(scope="module")
def spark_handler() -> SparkHandler:
    """
    Фикстура для инициализации SparkHandler.
    """
    return SparkHandler(DB_URL, DB_PROPERTIES)


def test_handler_has_spark_session(spark_handler: SparkHandler):
    """
    Проверка, что SparkHandler имеет корректный SparkSession.
    """
    from pyspark.sql import SparkSession

    spark = spark_handler.spark
    assert isinstance(spark, SparkSession), "SparkHandler не содержит SparkSession"

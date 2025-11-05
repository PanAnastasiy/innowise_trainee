from pyspark.sql import SparkSession

from TASKS.task_5.handlers.spark_handler import SparkLocalConnection


def test_singleton_instance():
    """
    Проверка, что SparkLocalConnection реализует паттерн Singleton.
    """
    instance1 = SparkLocalConnection()
    instance2 = SparkLocalConnection()

    assert instance1 is instance2, "Singleton работает некорректно: экземпляры разные"


def test_spark_session_initialized():
    """
    Проверка, что SparkSession успешно создаётся.
    """
    instance = SparkLocalConnection()
    spark: SparkSession = instance.get_session()

    assert isinstance(spark, SparkSession), "Не создан экземпляр SparkSession"
    assert spark.version is not None, "Версия Spark не определена"


def test_spark_session_can_read_empty_dataframe():
    """
    Проверка базовой работы SparkSession: создание пустого DataFrame.
    """
    spark = SparkLocalConnection().get_session()
    df = spark.createDataFrame([], "name STRING, age INT")
    result = df.collect()
    assert result == [], "Пустой DataFrame не должен содержать строк"

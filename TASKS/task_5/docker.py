import time

from pyspark.sql import SparkSession


def create_spark_session():
    """Создает Spark сессию с повторными попытками"""
    max_retries = 3
    retry_delay = 10  # секунды

    for attempt in range(max_retries):
        try:
            spark = (
                SparkSession.builder.appName("DockerSparkApp")
                .master("spark://localhost:7077")
                .config("spark.executor.memory", "1g")
                .config("spark.driver.memory", "1g")
                .config("spark.sql.adaptive.enabled", "true")
                .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
                .getOrCreate()
            )

            # Проверяем, что Spark действительно работает
            spark.sparkContext.parallelize([1, 2, 3, 4, 5]).count()
            print("✅ Успешное подключение к Spark cluster!")
            return spark

        except Exception as e:
            print(f"❌ Попытка {attempt + 1} не удалась: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Повторная попытка через {retry_delay} секунд...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Не удалось подключиться к Spark после {max_retries} попыток")


# Использование
try:
    spark = create_spark_session()

    # Пример работы с данными
    df = spark.range(1000).toDF("id")
    print(f"Количество записей: {df.count()}")

    # Создание более сложного DataFrame
    sample_data = [
        ("IT", "Москва", 5000),
        ("Finance", "Санкт-Петербург", 4500),
        ("HR", "Новосибирск", 3500),
        ("IT", "Екатеринбург", 4800),
        ("Marketing", "Казань", 4000),
    ]

    employees_df = spark.createDataFrame(sample_data, ["department", "city", "salary"])

    print("Данные сотрудников:")
    employees_df.show()

    # Агрегация данных
    print("Средняя зарплата по отделам:")
    employees_df.groupBy("department").avg("salary").show()

    spark.stop()

except Exception as e:
    print(f"Ошибка: {e}")

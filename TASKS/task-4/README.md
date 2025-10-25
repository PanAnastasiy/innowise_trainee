# Task 4 — Анализ данных о студентах и комнатах

Проект выполняет анализ данных о студентах и их распределении по комнатам, используя PostgreSQL в качестве базы данных.  
Результаты сохраняются в форматах **JSON** и **XML**.

---

## 📂 Структура решения

## 📂 Структура решения

task-4/
│
├── data_manager/ # Логика обработки данных и формирования отчётов
│ ├── init.py
│ ├── executer.py # SQL-запросы к БД (Executor)
│ └── reporter.py # Классы для сохранения данных в JSON и XML
│
├── handlers/ # Работа с БД и JSON-файлами
│ ├── init.py
│ ├── db_handler.py # Подключение к PostgreSQL (DBConnection)
│ └── json_handler.py # Загрузка JSON-данных в таблицы (JSONHandler)
│
├── sql/ # SQL-скрипты для подготовки базы данных
│ ├── students-schema.sql # Создание таблиц student и room
│ ├── create-indexes.sql # Индексы для ускорения запросов
│ └── queries.sql # Примеры аналитических запросов
│
├── main.py # Точка входа: загрузка данных, анализ, сохранение в форматы JSON и XML
└── README.md # Документация решения


####  *  1. Using PostgreSQL database to create a data schema corresponding to the files in the attachment

Был создан скрипт для генерации базы данных, согласно схеме связей в json-файлах - **`students-schema.sql`**.

####  *  2. Write a script to load these two files and write data to the database.

Были созданы классы обработчики для соединения (**DBConnection**) и загрузки данных (**JSONHandler**) в бд.

####  *  3. Write necessary queries to the database

Был создан скрипт для реализации запросов к бд с анализом их выполнения - **`queries.sql`**.

####  *  4. Propose options for optimizing queries using indexes. As a result we need to generate a SQL query that adds the required indexes.

Для ускорения выполнения запросов добавлены индексы в **`create-indexes.sql`**
По итогу запросы выполняются значительно быстрее за счёт оптимизированных индексов.

####  *  5. Unload the result in JSON or XML format

Были реализованы классы для корректного форматирования и сохранения в нужный формат результатов SQL-запросов (**JSONReporter** и **XMLReporter**).

####  *  6. The command interface should support some input parameters

Архитектура решения разработана с использованием принципов ООП и SOLID, обеспечивая четкое разделение ответственности.

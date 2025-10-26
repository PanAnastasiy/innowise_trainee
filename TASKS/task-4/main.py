from TASKS.consts import STUDENT_JSON_PATH, ROOM_JSON_PATH, RESOURCE_DIR
from handlers import *
from data_manager import *

# Загрузка данных из JSON в базу данных
with DBConnection() as student_db:
    json_handler = JSONHandler(student_db, ROOM_JSON_PATH, STUDENT_JSON_PATH)

    # Тот самый маппинг объектов JSON-файла и таблиц
    json_handler.load_data_to_db({ROOM_JSON_PATH: 'room', STUDENT_JSON_PATH: 'student'})

# Выполнение SQL-запросов для последующей записи в файлы XML и JSON
with DBConnection() as student_db:
    executor = Executer(student_db)

    results = {
        "rooms_count_students": executor.list_rooms_count_students(),
        "rooms_smallest_avg_age": executor.rooms_smallest_avg_age(),
        "rooms_largest_age_diff": executor.rooms_largest_age_diff(),
        "rooms_different_sex": executor.rooms_different_sex(),
        "rooms_same_sex": executor.rooms_same_sex(),
    }

# Запись результов запросов в файлы
reporter = JSONReporter()
reporter.save(results, f"{RESOURCE_DIR}/json/report.json")

reporter = XMLReporter()
reporter.save(results, f"{RESOURCE_DIR}/xml/report.xml")

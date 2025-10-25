from consts import STUDENT_JSON_PATH, ROOM_JSON_PATH, RESOURCE_DIR
from handlers import *
from executer import *
from reporter import *

with DBConnection() as student_db:
    json_handler = JSONHandler(student_db, ROOM_JSON_PATH, STUDENT_JSON_PATH)
    json_handler.load_data_to_db({
        ROOM_JSON_PATH: 'room',
        STUDENT_JSON_PATH: 'student'
    })


with DBConnection() as student_db:
    queries_results = Executer(student_db)

    results = {
        "rooms_count_students": queries_results.list_rooms_count_students(),
        "rooms_smallest_avg_age": queries_results.rooms_smallest_avg_age(),
        "rooms_largest_age_diff": queries_results.rooms_largest_age_diff(),
        "rooms_different_sex": queries_results.rooms_different_sex(),
        "rooms_same_sex": queries_results.rooms_same_sex()
    }


reporter = JSONReporter()
reporter.save(results, f"{RESOURCE_DIR}/json/report.json")

reporter = XMLReporter()
reporter.save(results, f"{RESOURCE_DIR}/xml/report.xml")

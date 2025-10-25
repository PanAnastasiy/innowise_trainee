import argparse

from consts import RESOURCE_DIR
from handlers import *
from data_manager import *


class CLIMain:
    """
    CLI-запуск для обработки данных студентов и комнат.
    Параметры:
    - students_path: str — путь к JSON-файлу со студентами
    - rooms_path: str — путь к JSON-файлу с комнатами
    - output_format: str — формат вывода ('json' или 'xml')
    """

    def __init__(self, students_path: str, rooms_path: str, output_format: str):
        self.students_path: str = students_path
        self.rooms_path: str = rooms_path
        self.output_format: str = output_format.lower()
        self.results: dict = {}

    def load_data(self) -> None:
        """Загрузка данных из JSON-файлов в базу данных."""
        with DBConnection() as db:
            handler = JSONHandler(db, self.rooms_path, self.students_path)
            handler.load_data_to_db({
                self.rooms_path: 'room',
                self.students_path: 'student'
            })

    def execute_queries(self) -> None:
        """Выполнение SQL-запросов и сохранение результатов в self.results."""
        with DBConnection() as db:
            executor = Executer(db)
            self.results = {
                "rooms_count_students": executor.list_rooms_count_students(),
                "rooms_smallest_avg_age": executor.rooms_smallest_avg_age(),
                "rooms_largest_age_diff": executor.rooms_largest_age_diff(),
                "rooms_different_sex": executor.rooms_different_sex(),
                "rooms_same_sex": executor.rooms_same_sex()
            }

    def save_results(self) -> None:
        """Сохранение результатов в выбранный формат (JSON или XML)."""
        output_path = f"{RESOURCE_DIR}/{self.output_format}/report.{self.output_format}"
        if self.output_format == 'json':
            reporter = JSONReporter()
        elif self.output_format == 'xml':
            reporter = XMLReporter()
        else:
            raise ValueError("Format must be 'json' or 'xml'")
        reporter.save(self.results, output_path)

    def run(self) -> None:
        """Запуск всех этапов приложения: загрузка, запросы, сохранение."""
        self.load_data()
        self.execute_queries()
        self.save_results()


def main() -> None:
    """
    Точка входа для CLI-запуска.
    Пример запуска:
    python TASKS/task-4/cli_main.py --students ../../resources/json/students.json --rooms ../../resources/json/rooms.json --format json
    python TASKS/task-4/cli_main.py --students ../../resources/json/students.json --rooms ../../resources/json/rooms.json --format xml
    """
    parser = argparse.ArgumentParser(description="Student-Room Data Processor")
    parser.add_argument('--students', required=True, help="Path to students JSON file")
    parser.add_argument('--rooms', required=True, help="Path to rooms JSON file")
    parser.add_argument('--format', required=True, choices=['json', 'xml'], help="Output format")
    args = parser.parse_args()
    app = CLIMain(args.students, args.rooms, args.format)
    app.run()


if __name__ == "__main__":
    main()

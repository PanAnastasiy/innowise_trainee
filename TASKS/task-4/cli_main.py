import argparse
import os
import sys

# Не видит папки за рамками задания, приходится подключать корень проекта
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from data_manager.executer import Executer
from data_manager.reporter import JSONReporter, XMLReporter
from handlers.db_handler import DBConnection
from handlers.json_handler import JSONHandler


class CLIApp:
    """
    CLI-приложение для обработки данных студентов и комнат.

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
            handler.load_data_to_db({self.rooms_path: 'rooms', self.students_path: 'students'})

    def execute_queries(self) -> None:
        """Выполнение SQL-запросов и сохранение результатов в self.results."""
        with DBConnection() as db:
            executor = Executer(db)
            self.results = {
                "rooms_count_students": executor.list_rooms_count_students(),
                "rooms_smallest_avg_age": executor.rooms_smallest_avg_age(),
                "rooms_largest_age_diff": executor.rooms_largest_age_diff(),
                "rooms_different_sex": executor.rooms_different_sex(),
                "rooms_same_sex": executor.rooms_same_sex(),
            }

    def save_results(self) -> None:
        """Сохранение результатов в выбранный формат (JSON или XML)."""
        output_dir = os.path.join("resources", self.output_format)
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"report.{self.output_format}")

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
    Точка входа для CLI-приложения.

    python TASKS/task-4/cli_main.py --students "resources/json/students.json" --rooms "resources/json/rooms.json" --format json
    python TASKS/task-4/cli_main.py --students "resources/json/students.json" --rooms "resources/json/rooms.json" --format xml
    """
    parser = argparse.ArgumentParser(description="Student-Room Data Processor")
    parser.add_argument('--students', required=True, help="Path to students JSON file")
    parser.add_argument('--rooms', required=True, help="Path to rooms JSON file")
    parser.add_argument('--format', required=True, choices=['json', 'xml'], help="Output format")
    args = parser.parse_args()

    app = CLIApp(args.students, args.rooms, args.format)
    app.run()


if __name__ == "__main__":
    main()

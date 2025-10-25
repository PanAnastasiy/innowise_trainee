import json
import os
from dotenv import load_dotenv
from .db_handler import DBConnection
from utils.design import Message, Color

load_dotenv()

class JSONHandler:

    def __init__(self, db: DBConnection, *json_files: str) -> None:
        self.db = db
        self.data = {}
        base_dir = os.path.dirname(__file__)
        project_root = os.path.join(base_dir, "../../..")

        # Загружаем JSON-файлы в память
        for file_path in json_files:
            rel_path = os.path.join(project_root, file_path)
            with open(rel_path, 'r', encoding='utf-8') as f:
                self.data[file_path] = json.load(f)

    def load_data_to_db(self, mapping: dict[str, str]):
        """
        mapping: словарь вида {json_file_path: table_name}
        """
        for file_path, table_name in mapping.items():
            if file_path not in self.data:
                Message.print_message(f"Файл {file_path} не найден!",
                                      Color.RED, Color.LIGHT_WHITE)
                continue

            records = self.data[file_path]
            if not records:

                Message.print_message(f"Файл {file_path} не содержит ни одной записи!",
                                      Color.YELLOW, Color.LIGHT_WHITE)
                continue

            # Формируем список колонок и placeholders
            columns = records[0].keys()
            columns_str = ", ".join(columns)
            placeholders = ", ".join([f"%({col})s" for col in columns])
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            try:
                for record in records:
                    self.db.execute(query, record)
                Message.print_message(f"Данные из {file_path} успешно загружены в {table_name}!",
                                      Color.BLUE, Color.LIGHT_WHITE)
            except Exception as e:
                Message.print_message(f"Ошибка при загрузке данных из {file_path} в {table_name}: {e}!",
                                      Color.RED, Color.LIGHT_WHITE)
                raise

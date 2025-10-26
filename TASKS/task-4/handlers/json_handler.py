import json
import os
from dotenv import load_dotenv
from .db_handler import DBConnection
from TASKS.utils.design import Message, Color

load_dotenv()


class JSONHandler:
    """
    Класс для записи данных из json в базу данных.

    Позволяет:
    - загружать несколько АБСОЛЮТНО ЛЮБЫХ JSON-файлов сразу при инициалзиации объекта;
    - хранить их содержимое в памяти;
    - записывать данные в указанные таблицы базы данных с помощью DBConnection.
    - важно понимать, что структура JSON-файла и соответствующей таблицы должна быть одинаковой,
     поскольку добавление записей в таблицу идёт по полю json-файла
      (В students.json ссылка на комнаты в виде поля room), да это своего рода косяк, но реализация прикольная :)
    """

    def __init__(self, db: DBConnection, *json_files: str) -> None:
        """
        Инициализирует обработчик, загружая указанные JSON-файлы в память
        с предварительной установкой соединения с бд.
        """
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
        Загружает данные из памяти в таблицы базы данных.

        Параметры:
        ----------
        mapping : dict[str, str]
            Словарь соответствий: { "путь_к_json_файлу": "имя_таблицы" }.
        """
        for file_path, table_name in mapping.items():
            if file_path not in self.data:
                Message.print_message(f"Файл {file_path} не найден!", Color.RED, Color.LIGHT_WHITE)
                continue

            records = self.data[file_path]
            if not records:

                Message.print_message(
                    f"Файл {file_path} не содержит ни одной записи!",
                    Color.YELLOW,
                    Color.LIGHT_WHITE,
                )
                continue

            # Для формирования параметризированного INSERT-запроса приходиться сделать некие преобразования
            columns = records[0].keys()
            columns_str = ", ".join(columns)
            placeholders = ", ".join([f"%({col})s" for col in columns])
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            try:
                for record in records:
                    self.db.execute(query, record)
                Message.print_message(
                    f"Данные из {file_path} успешно загружены в {table_name}!",
                    Color.BLUE,
                    Color.LIGHT_WHITE,
                )
            except Exception as e:
                Message.print_message(
                    f"Ошибка при загрузке данных из {file_path} в {table_name}: {e}!",
                    Color.RED,
                    Color.LIGHT_WHITE,
                )
                raise

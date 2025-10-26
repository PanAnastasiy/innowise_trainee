from typing import Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.design import Message, Color
import os
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    """
    Класс для управления соединением с базой данных PostgreSQL.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.host = host or os.getenv("STUDENT_DB_HOST")
        self.port = port or int(os.getenv("STUDENT_DB_PORT"))
        self.database = database or os.getenv("STUDENT_DB_NAME")
        self.user = user or os.getenv("STUDENT_PG_USER")
        self.password = password or os.getenv("STUDENT_PG_PASSWORD")
        self.conn = None
        self.cursor = None

    def __enter__(self) -> "DBConnection":
        """
        Открывает соединение при входе в контекстный менеджер (`with`).
        Возвращает объект DBConnection для выполнения запросов.
        """
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            Message.print_message(
                "Соединение с базой данных успешно установлено.", Color.GREEN, Color.LIGHT_WHITE
            )
            return self
        except Exception as e:
            Message.print_message(
                f"Ошибка подключения к базе данных: {e}", Color.RED, Color.LIGHT_WHITE
            )
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Закрывает соединение и курсор при выходе из контекста.
        Вызывается автоматически после завершения блока `with`.
        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

        Message.print_message(
            "Соединение с базой данных успешно закрыто.", Color.BLUE, Color.LIGHT_WHITE
        )

    def execute(
        self, query: str, params: Optional[tuple[Any, ...]] = None
    ) -> Optional[list[dict[str, Any]]]:
        """
        Выполняет SQL-запрос.

        :param query: SQL-запрос в виде строки.
        :param params: Кортеж параметров для подстановки (опционально).
        :return: Результаты выборки (list[dict]) для SELECT-запросов, иначе None.
        :raises RuntimeError: если соединение не установлено.
        :raises Exception: если запрос завершился с ошибкой.
        """
        if not self.conn:
            raise RuntimeError(
                "Соединение с БД не установлено. Используйте 'with DBConnection() as db:'"
            )

        try:
            self.cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            Message.print_message(f"Ошибка выполнения запроса: {e}", Color.RED, Color.LIGHT_WHITE)
            raise

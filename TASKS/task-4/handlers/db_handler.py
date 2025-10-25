from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.design import Message, Color
import os
from dotenv import load_dotenv

load_dotenv()

class DBConnection:
    def __init__(self, host=None, port=None, database=None, user=None, password=None):
        # Если параметры не переданы, берём их из .env
        self.host = host or os.getenv("STUDENT_DB_HOST", "localhost")
        self.port = port or int(os.getenv("STUDENT_DB_PORT", 5432))
        self.database = database or os.getenv("STUDENT_DB_NAME", "student_db")
        self.user = user or os.getenv("STUDENT_PG_USER", "root")
        self.password = password or os.getenv("STUDENT_PG_PASSWORD", "root")

        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Открывает соединение при входе в with"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            Message.print_message("Соединение с базой данных успешно установлено.",
                                  Color.GREEN, Color.LIGHT_WHITE)
            return self
        except Exception as e:
            Message.print_message(f"Ошибка подключения к базе данных: {e}",
                                  Color.RED, Color.LIGHT_WHITE)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрывает соединение при выходе из with"""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None
        Message.print_message("Соединение с базой данных успешно закрыто.",
                              Color.BLUE, Color.LIGHT_WHITE)

    def execute(self, query, params=None) -> list[Any]:
        """Выполняет SQL-запрос (SELECT, INSERT, UPDATE, DELETE)."""
        if not self.conn:
            raise RuntimeError("Соединение с БД не установлено. Используйте 'with DBConnection() as db:'")
        try:
            self.cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            Message.print_message(f"Ошибка выполнения запроса: {e}",
                                  Color.RED, Color.LIGHT_WHITE)
            raise

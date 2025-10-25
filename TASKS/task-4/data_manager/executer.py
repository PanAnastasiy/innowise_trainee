from typing import Any

class Executer:
    """
    Класс Executer выполняет SQL-запросы для последущей записи результатов в json и xml формат.
    """

    def __init__(self, db) -> None:
        self.db = db

    def list_rooms_count_students(self) -> list[dict[str, Any]]:
        """
        Возвращает список комнат и количество студентов в каждой из них.

        :return: Список словарей, где каждый элемент содержит номер комнаты и число студентов.
        """
        return self.db.execute("""
                               SELECT room.name AS "Room's number",
                                      COUNT(student.id) AS "Count of students in room"
                               FROM room
                                        LEFT JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               ORDER BY "Count of students in room" DESC
                               """)

    def rooms_smallest_avg_age(self, limit: int = 5) -> list[dict[str, Any]]:
        """
        Возвращает список комнат с наименьшим средним возрастом студентов.

        :param limit: Количество записей для вывода (по умолчанию 5).
        :return: Список словарей с названием комнаты и средним возрастом студентов.
        """
        return self.db.execute(f"""
            SELECT room.name AS "Room's number",
                   ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, student.birthday))), 2) AS "Average age of students"
            FROM room
                     JOIN student ON room.id = student.room
            GROUP BY room.id, room.name
            ORDER BY "Average age of students"
            LIMIT {limit}
        """)

    def rooms_largest_age_diff(self, limit: int = 5) -> list[dict[str, Any]]:
        """
        Возвращает список комнат с наибольшей разницей в возрасте студентов.

        :param limit: Количество записей для вывода (по умолчанию 5).
        :return: Список словарей с названием комнаты и разницей в возрасте студентов.
        """
        return self.db.execute(f"""
            SELECT room.name AS "Room's number",
                   EXTRACT(YEAR FROM AGE(MAX(student.birthday), MIN(student.birthday))) AS "Difference in the age of students"
            FROM room
                     JOIN student ON room.id = student.room
            GROUP BY room.id, room.name
            ORDER BY "Difference in the age of students" DESC
            LIMIT {limit}
        """)

    def rooms_different_sex(self) -> list[dict[str, Any]]:
        """
        Возвращает список комнат, где живут студенты разного пола.

        :return: Список словарей с названиями комнат, где проживают студенты обоих полов.
        """
        return self.db.execute("""
                               SELECT room.name AS "List of rooms where different-sex students live"
                               FROM room
                                        JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               HAVING COUNT(DISTINCT student.sex) = 2
                               """)

    def rooms_same_sex(self) -> list[dict[str, Any]]:
        """
        Возвращает список комнат, где живут студенты одного пола.

        :return: Список словарей с названиями комнат, где проживают студенты одного пола.
        """
        return self.db.execute("""
                               SELECT room.name AS "List of rooms where same-sex students live"
                               FROM room
                                        JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               HAVING COUNT(DISTINCT student.sex) = 1
                               """)

class Executer:
    def __init__(self, db):
        self.db = db

    # List of rooms and the number of students in each of them
    def list_rooms_count_students(self):
        return self.db.execute("""
                               SELECT room.name AS "Room's number",
                                      COUNT(student.id) AS "Count of students in room"
                               FROM room
                                        LEFT JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               ORDER BY "Count of students in room" DESC
                               """)

    # 5 rooms with the smallest average age of students
    def rooms_smallest_avg_age(self, limit=5):
        return self.db.execute(f"""
            SELECT room.name AS "Room's number",
                   ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, student.birthday))), 2) AS "Average age of students"
            FROM room
                     JOIN student ON room.id = student.room
            GROUP BY room.id, room.name
            ORDER BY "Average age of students"
            LIMIT {limit}
        """)

    # 5 rooms with the largest difference in the age of students
    def rooms_largest_age_diff(self, limit=5):
        return self.db.execute(f"""
            SELECT room.name AS "Room's number",
                   EXTRACT(YEAR FROM AGE(MAX(student.birthday), MIN(student.birthday))) AS "Difference in the age of students"
            FROM room
                     JOIN student ON room.id = student.room
            GROUP BY room.id, room.name
            ORDER BY "Difference in the age of students" DESC
            LIMIT {limit}
        """)

    # List of rooms where different-sex students live
    def rooms_different_sex(self):
        return self.db.execute("""
                               SELECT room.name AS "List of rooms where different-sex students live"
                               FROM room
                                        JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               HAVING COUNT(DISTINCT student.sex) = 2
                               """)

    # List of rooms where same-sex students live
    def rooms_same_sex(self):
        return self.db.execute("""
                               SELECT room.name AS "List of rooms where same-sex students live"
                               FROM room
                                        JOIN student ON room.id = student.room
                               GROUP BY room.id, room.name
                               HAVING COUNT(DISTINCT student.sex) = 1
                               """)

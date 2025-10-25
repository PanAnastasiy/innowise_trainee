
-- List of rooms and the number of students in each of them

EXPLAIN ANALYZE
SELECT room.name AS "Room's number",
       COUNT(student.id) AS "Count of students in room"
FROM room
    LEFT JOIN student ON room.id = student.room
GROUP BY room.id, room.name
ORDER BY 2 DESC;

/*
Without Indexes:
Planning Time: 0.351 ms
Execution Time: 5.710 ms
*/


-- 5 rooms with the smallest average age of students

EXPLAIN ANALYZE
SELECT room.name AS "Room's number",
       ROUND(AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, student.birthday))), 2) AS "Average age of students"
FROM room
    JOIN student ON room.id = student.room
GROUP BY room.id, room.name
ORDER BY 2
LIMIT 5;

/*
Without Indexes:
Planning Time: 0.285 ms
Execution Time: 7.492 ms
*/


-- 5 rooms with the largest difference in the age of students

EXPLAIN ANALYZE
SELECT
    room.name AS "Room's number",
    EXTRACT(YEAR FROM AGE(MAX(student.birthday), MIN(student.birthday))) AS "Difference in the age of students"
FROM room
         JOIN student ON room.id = student.room
GROUP BY room.id, room.name
ORDER BY "Difference in the age of students" DESC
LIMIT 5;

/*
Without Indexes:
Planning Time: 0.176 ms
Execution Time: 4.266 ms
*/

SELECT *
FROM room
         JOIN student ON room.id = student.room
WHERE room.id = 875;


-- List of rooms where different-sex students live

EXPLAIN ANALYZE
SELECT room.name AS "List of rooms where different-sex students live"
FROM room
         JOIN student ON room.id = student.room
GROUP BY room.id, room.name
HAVING COUNT(DISTINCT sex) = 2;

/*
Without Indexes:
Planning Time: 0.141 ms
Execution Time: 8.465 ms

*/


-- List of rooms where same-sex students live

EXPLAIN ANALYZE
SELECT room.name AS "List of rooms where same-sex students live"
FROM room
         JOIN student ON room.id = student.room
GROUP BY room.id, room.name
HAVING COUNT(DISTINCT sex) = 1;

/*
Without Indexes:
Planning Time: 0.155 ms
Execution Time: 7.741 ms
*/

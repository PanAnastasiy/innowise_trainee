/*
 Для аналитики комнат с большим числом студентов:

student.room_id — для JOIN → ускоряет подсчёт студентов по комнатам.

student.birthday — для AVG, MIN, MAX → ускоряет расчёт возраста.

student.sex — для COUNT DISTINCT → ускоряет проверку пола в комнатах.

*/

-- Индекс для соединения student ↔ room
CREATE INDEX idx_student_room_id ON student(room);

-- Индекс для поиска по дате рождения (avg_age, age_diff)
CREATE INDEX idx_student_birthday ON student(birthday);

-- Индекс по полу (sex)
CREATE INDEX idx_student_sex ON student(sex);

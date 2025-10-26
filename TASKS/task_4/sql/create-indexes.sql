
-- Стандартный индекс для ускорения соединений между таблицами student и room
CREATE INDEX idx_student_room_id ON student(room);

-- Стандартный индекс для оптимизации запросов, где выполняются вычисления по возрасту студентов

CREATE INDEX idx_student_birthday ON student(birthday);

-- Стандартный индекс для ускорения агрегаций и фильтрации по полу студентов
CREATE INDEX idx_student_sex ON student(sex);

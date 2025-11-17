-- Standard index to speed up joins between student and room tables
CREATE INDEX idx_student_room_id ON student(room);

-- Standard index to optimize queries calculating student age
CREATE INDEX idx_student_birthday ON student(birthday);

-- Standard index to accelerate aggregations and filtering by student sex
CREATE INDEX idx_student_sex ON student(sex);

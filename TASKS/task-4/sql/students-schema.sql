CREATE TABLE room (
                      id SERIAL PRIMARY KEY,
                      name VARCHAR(255) NOT NULL
);

CREATE TABLE student (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR(255) NOT NULL,
                         sex CHAR(1),
                         birthday DATE,
                         room INT,
                         FOREIGN KEY (room) REFERENCES room(id)
                             ON DELETE SET NULL
                             ON UPDATE CASCADE
);
from consts import STUDENT_JSON_PATH, ROOM_JSON_PATH
from handlers import *


'''
1. Using MySQL database (or other relational database, for example, PostgreSQL)
to create a data schema corresponding to the files in the attachment
(many-to-one relationship)

DATA SCHEMA - students-schema.sql
'''


# 2. Write a script to load these two files and write data to the database

with DBConnection() as student_db:
    json_handler = JSONHandler(student_db, ROOM_JSON_PATH, STUDENT_JSON_PATH)
    json_handler.load_data_to_db({
        ROOM_JSON_PATH: 'room',
        STUDENT_JSON_PATH: 'student'
    })

#-------------------------------------------------------------------------------

# 3. Necessary queries to the database - queries.sql
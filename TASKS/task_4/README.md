# Task 4 — Student and Room Data Analysis

This project performs analysis of students and their room assignments using **PostgreSQL** as the database.
The results are exported in **JSON** and **XML** formats.

---

#### 1. Using PostgreSQL database to create a data schema corresponding to the files in the attachment

A script was created to generate the database according to the relationships in the JSON files — **`students-schema.sql`**.

---

#### 2. Write a script to load these two files and write data to the database

Handler classes were implemented for database connections (**DBConnection**) and loading JSON data into the database (**JSONHandler**).

---

#### 3. Write necessary queries to the database

A script was created to implement queries on the database and analyze their results — **`queries.sql`**.

---

#### 4. Propose options for optimizing queries using indexes. As a result we need to generate a SQL query that adds the required indexes

Indexes were added to improve query performance — **`create-indexes.sql`**.
As a result, the queries run significantly faster due to optimized indexing.

---

#### 5. Unload the result in JSON or XML format

Classes were implemented for correctly formatting and saving SQL query results in the desired output format (**JSONReporter** and **XMLReporter**).

---

#### 6. The command interface should support some input parameters

The solution architecture follows **OOP** and **SOLID** principles, providing a clear separation of responsibilities.

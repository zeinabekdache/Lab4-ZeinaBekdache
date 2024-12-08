"""
Database Management Module

This module provides a utility class, `DatabaseManager`, for managing
a school database. It includes functionality for creating tables,
CRUD operations for students, instructors, and courses, as well as
registration and search functionality.

:module: database_manager
"""

import sqlite3


class DatabaseManager:
    """
    A class to manage database operations for a school system.

    Handles SQLite database connections and operations for students,
    instructors, courses, and registrations.

    :param db_name: The name of the database file (default: "school_data.db")
    :type db_name: str
    """
    def __init__(self, db_name="school_data.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Creates the required database tables if they do not exist.

        Tables created:
        - students
        - instructors
        - courses
        - registrations

        :return: None
        """
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS instructors (
                    instructor_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    instructor_id TEXT,
                    FOREIGN KEY (instructor_id)
                        REFERENCES instructors (instructor_id)
                        ON DELETE SET NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS registrations (
                    student_id TEXT,
                    course_id TEXT,
                    PRIMARY KEY (student_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                        ON DELETE CASCADE
                )
            """)

    def add_student(self, student_id, name, age, email):
        """
        Adds a student to the database.

        :param student_id: The unique identifier for the student
        :type student_id: str
        :param name: The name of the student
        :type name: str
        :param age: The age of the student
        :type age: int
        :param email: The email address of the student
        :type email: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                INSERT INTO students (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
            """, (student_id, name, age, email))

    def get_students(self):
        """
        Retrieves all students from the database.

        :return: A list of all students
        :rtype: list of tuple
        """
        with self.connection:
            return self.connection.execute("SELECT * FROM students").fetchall()

    def update_student(self, student_id, name, age, email):
        """
        Updates a student's details in the database.

        :param student_id: The unique identifier for the student
        :type student_id: str
        :param name: The updated name of the student
        :type name: str
        :param age: The updated age of the student
        :type age: int
        :param email: The updated email address of the student
        :type email: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                UPDATE students
                SET name = ?, age = ?, email = ?
                WHERE student_id = ?
            """, (name, age, email, student_id))

    def delete_student(self, student_id):
        """
        Deletes a student from the database.

        :param student_id: The unique identifier for the student to delete
        :type student_id: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                DELETE FROM students
                WHERE student_id = ?
            """, (student_id,))

    # Instructor CRUD Operations
    def add_instructor(self, instructor_id, name, age, email):
        """
        Adds an instructor to the database.

        :param instructor_id: The unique identifier for the instructor
        :type instructor_id: str
        :param name: The name of the instructor
        :type name: str
        :param age: The age of the instructor
        :type age: int
        :param email: The email address of the instructor
        :type email: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
            """, (instructor_id, name, age, email))

    def get_instructors(self):
        """
        Retrieves all instructors from the database.

        :return: A list of all instructors
        :rtype: list of tuple
        """
        with self.connection:
            return self.connection.execute("SELECT * FROM instructors").fetchall()

    def update_instructor(self, instructor_id, name, age, email):
        """
        Updates an instructor's details in the database.

        :param instructor_id: The unique identifier for the instructor
        :type instructor_id: str
        :param name: The updated name of the instructor
        :type name: str
        :param age: The updated age of the instructor
        :type age: int
        :param email: The updated email address of the instructor
        :type email: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                UPDATE instructors
                SET name = ?, age = ?, email = ?
                WHERE instructor_id = ?
            """, (name, age, email, instructor_id))

    def delete_instructor(self, instructor_id):
        """
        Deletes an instructor from the database.

        :param instructor_id: The unique identifier for the instructor to delete
        :type instructor_id: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                DELETE FROM instructors
                WHERE instructor_id = ?
            """, (instructor_id,))

    # Course CRUD Operations
    def add_course(self, course_id, course_name, instructor_id=None):
        """
        Adds a course to the database.

        :param course_id: The unique identifier for the course
        :type course_id: str
        :param course_name: The name of the course
        :type course_name: str
        :param instructor_id: The ID of the instructor assigned to the course (default: None)
        :type instructor_id: str, optional
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                INSERT INTO courses (course_id, course_name, instructor_id)
                VALUES (?, ?, ?)
            """, (course_id, course_name, instructor_id))

    def get_courses(self):
        """
        Retrieves all courses along with their instructor's name (if assigned).

        :return: A list of all courses with instructor details
        :rtype: list of tuple
        """
        with self.connection:
            return self.connection.execute("""
                SELECT c.course_id, c.course_name, i.name AS instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            """).fetchall()

    def update_course(self, course_id, course_name, instructor_id=None):
        """
        Updates a course's details in the database.

        :param course_id: The unique identifier for the course
        :type course_id: str
        :param course_name: The updated name of the course
        :type course_name: str
        :param instructor_id: The updated instructor ID for the course (default: None)
        :type instructor_id: str, optional
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                UPDATE courses
                SET course_name = ?, instructor_id = ?
                WHERE course_id = ?
            """, (course_name, instructor_id, course_id))

    def delete_course(self, course_id):
        """
        Deletes a course from the database.

        :param course_id: The unique identifier for the course to delete
        :type course_id: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                DELETE FROM courses
                WHERE course_id = ?
            """, (course_id,))

    # Registration Operations
    def register_student(self, student_id, course_id):
        """
        Registers a student for a course.

        :param student_id: The unique identifier for the student
        :type student_id: str
        :param course_id: The unique identifier for the course
        :type course_id: str
        :return: None
        """
        with self.connection:
            self.connection.execute("""
                INSERT OR IGNORE INTO registrations (student_id, course_id)
                VALUES (?, ?)
            """, (student_id, course_id))

    def get_student_courses(self, student_id):
        """
        Retrieves all courses a student is registered for.

        :param student_id: The unique identifier for the student
        :type student_id: str
        :return: A list of courses the student is registered in
        :rtype: list of tuple
        """
        with self.connection:
            return self.connection.execute("""
                SELECT c.course_id, c.course_name
                FROM courses c
                JOIN registrations r ON c.course_id = r.course_id
                WHERE r.student_id = ?
            """, (student_id,)).fetchall()

    def update_student_registrations(self, student_id, course_ids):
        """
        Updates a student's course registrations.

        Removes all current registrations for the student and adds new ones.

        :param student_id: The unique identifier for the student
        :type student_id: str
        :param course_ids: A list of course IDs to register the student in
        :type course_ids: list of str
        :return: None
        """
        with self.connection:
            # Remove all current registrations for the student
            self.connection.execute("""
                DELETE FROM registrations
                WHERE student_id = ?
            """, (student_id,))

            # Add new registrations
            for course_id in course_ids:
                self.register_student(student_id, course_id)

    def search_records(self, query):
        """
        Searches for records matching the query in students, instructors, and courses.

        :param query: The search term
        :type query: str
        :return: A list of matching records from students, instructors, and courses
        :rtype: list of tuple
        """
        with self.connection:
            results = []

            # Search students
            student_results = self.connection.execute("""
                SELECT 'Student' as type, * FROM students
                WHERE name LIKE ? OR student_id LIKE ? OR email LIKE ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
            results.extend(student_results)

            # Search instructors
            instructor_results = self.connection.execute("""
                SELECT 'Instructor' as type, * FROM instructors
                WHERE name LIKE ? OR instructor_id LIKE ? OR email LIKE ?
            """, (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
            results.extend(instructor_results)

            # Search courses
            course_results = self.connection.execute("""
                SELECT 'Course' as type, c.*, i.name as instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                WHERE c.course_name LIKE ? OR c.course_id LIKE ?
            """, (f'%{query}%', f'%{query}%')).fetchall()
            results.extend(course_results)

            return results

    def close_connection(self):
        """
        Closes the database connection.

        :return: None
        """
        self.connection.close()

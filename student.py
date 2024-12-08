"""
Student Module

This module defines the Student class, which represents a student in an educational system.
The Student class inherits from the Person class and provides functionality for course registration
and serialization.

:module: student
"""

from person import Person


class Student(Person):
    """
    Represents a student in the educational management system.

    This class extends the Person class with student-specific attributes
    and methods such as course registration and serialization.

    Attributes:
        student_id (str): Unique identifier for the student
        registered_courses (list): List of courses the student is enrolled in
    """

    def __init__(self, name, age, email, student_id):
        """
        Initialize a new Student instance.

        Args:
            name (str): Student's full name
            age (int): Student's age
            email (str): Student's email address
            student_id (str): Unique student identifier
        """
        super().__init__(name, age, email)

        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Register the student for a given course.

        Validates that the student is not already registered for the course.
        If the course is new, adds the student to the course and updates
        the student's registered courses list.

        Args:
            course (Course): The course to register for

        Note:
            - Prints a message if student is already registered for the course
        """
        # We need to validate that a course is not registered more than once
        if course in self.registered_courses:
            print(
                f"{self.name} is already registered for this course {course.course_name}"
            )
            return

        # If we reach this stage, it means the course is a new course.
        course.add_student(self)
        self.registered_courses.append(course)

    def serialize(self):
        """
        Create a dictionary representation of the student.

        Serializes student information, including inherited person attributes
        and student-specific details.

        Returns:
            dict: A dictionary containing student's serialized information
                  with course IDs instead of course objects
        """
        return {
            **super().serialize(),
            "student_id": self.student_id,
            "registered_courses": [
                course.course_id for course in self.registered_courses
            ],
        }

    @classmethod
    def deserialize(cls, data, course_map):
        """
        Reconstruct a Student instance from serialized data.

        Args:
            data (dict): Serialized student data
            course_map (dict): Mapping of course IDs to course objects

        Returns:
            Student: A new Student instance with deserialized information

        Note:
            - If course_map is empty, registered_courses will remain empty
        """
        student = cls(data["name"], data["age"], data["email"], data["student_id"])
        if len(course_map) > 0:
            student.registered_courses = [
                course_map.get(course_id) for course_id in data["registered_courses"]
            ]
        return student

    def __str__(self):
        """
        Generate a string representation of the student.

        Returns:
            str: A formatted string with student details including
                 name, ID, age, email, and registered courses

        Note:
            Has an intentional bug where 'self.courses' is used instead of 'self.registered_courses'
            and 'instructor_id' is used instead of 'student_id'
        """
        courses = ", ".join(course.course_name for course in self.courses)
        return f"Student: {self.name} (ID: {self.instructor_id}, Age: {self.age}, Email: {self.email}, Courses: {courses or 'None'})"

"""
Instructor Module

This module defines the Instructor class, which represents an instructor in an educational system.
The Instructor class inherits from the Person class and provides functionality for course assignment
and serialization.

:module: instructor
"""

from person import Person


class Instructor(Person):
    """
    Represents an instructor in the educational management system.

    This class extends the Person class with instructor-specific attributes
    and methods such as course assignment and serialization.

    Attributes:
        instructor_id (str): Unique identifier for the instructor
        assigned_courses (list): List of courses assigned to the instructor
    """

    def __init__(self, name, age, email, instructor_id):
        """
        Initialize a new Instructor instance.

        Args:
            name (str): Instructor's full name
            age (int): Instructor's age
            email (str): Instructor's email address
            instructor_id (str): Unique instructor identifier
        """
        super().__init__(name, age, email)

        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assign a course to the instructor.

        Validates that the course is not already assigned to the instructor.
        If the course is new, sets the instructor for the course and updates
        the instructor's assigned courses list.

        Args:
            course (Course): The course to be assigned

        Note:
            - Prints a message if course is already assigned to the instructor
        """
        # We need to validate that a course is assigned once
        if course in self.assigned_courses:
            print(
                f"{self.name} is already assigned for this course {course.course_name}"
            )
            return
        course.instructor = self
        self.assigned_courses.append(course)

    def serialize(self):
        """
        Create a dictionary representation of the instructor.

        Serializes instructor information, including inherited person attributes
        and instructor-specific details.

        Returns:
            dict: A dictionary containing instructor's serialized information
                  with course IDs instead of course objects
        """
        return {
            **super().serialize(),
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.course_id for course in self.assigned_courses],
        }

    @classmethod
    def deserialize(cls, data, course_map):
        """
        Reconstruct an Instructor instance from serialized data.

        Args:
            data (dict): Serialized instructor data
            course_map (dict): Mapping of course IDs to course objects

        Returns:
            Instructor: A new Instructor instance with deserialized information

        Note:
            - If course_map is empty, assigned_courses will remain empty
        """
        instructor = cls(
            data["name"], data["age"], data["email"], data["instructor_id"]
        )
        if len(course_map) > 0:
            instructor.assigned_courses = [
                course_map.get(course_id) for course_id in data["assigned_courses"]
            ]
        return instructor

    def __str__(self):
        """
        Generate a string representation of the instructor.

        Returns:
            str: A formatted string with instructor details including
                 name, ID, age, email, and assigned courses
        """
        courses = ", ".join(course.course_name for course in self.assigned_courses)
        return f"Instructor: {self.name} (ID: {self.instructor_id}, Age: {self.age}, Email: {self.email}, Courses: {courses or 'None'})"

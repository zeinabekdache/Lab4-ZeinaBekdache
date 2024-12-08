"""
Course Management Module

This module provides a comprehensive Course class for managing course-related
information in an educational management system.

The module supports course creation, student enrollment, instructor assignment,
and data serialization/deserialization.

:module: course_management
"""


class Course:
    """
    Represents a course within an educational management system.

    This class provides functionality for managing course details,
    including student enrollment, instructor assignment, and serialization.

    :ivar course_id: Unique numerical identifier for the course
    :type course_id: int
    :ivar course_name: Full name of the course
    :type course_name: str
    :ivar instructor: Instructor assigned to the course
    :type instructor: Instructor, optional
    :ivar enrolled_students: List of students enrolled in the course
    :type enrolled_students: list
    """

    def __init__(self, course_id, course_name):
        """
        Initialize a new Course instance.

        Creates a course with a unique identifier and name,
        initializing empty instructor and student lists.

        :param course_id: Unique numerical identifier for the course
        :type course_id: int
        :param course_name: Full name of the course
        :type course_name: str
        :raises ValueError: If course name is less than two characters long after stripping whitespace
        """
        self.validate_course_name(course_name)
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

    def add_student(self, student):
        """
        Enroll a student in the course.

        Prevents duplicate student enrollments by checking existing enrollment.
        Prints a message if the student is already enrolled.

        :param student: Student object to be added to the course
        :type student: Student
        :raises TypeError: If the input is not a valid Student object
        :returns: None
        """
        if student in self.enrolled_students:
            print(
                f"{student.name} is already enrolled in this course {self.course_name}"
            )
            return

        self.enrolled_students.append(student)

    def validate_course_name(self, course_name):
        """
        Validate the length of the course name.

        Ensures the course name meets minimum length requirements
        after removing leading and trailing whitespace.

        :param course_name: Name of the course to validate
        :type course_name: str
        :raises ValueError: If course name is less than two characters long
        """
        if len(course_name.strip()) < 2:
            raise ValueError("course_name must be two or more characters")

    def serialize(self):
        """
        Convert course information to a serializable dictionary.

        Creates a dictionary representation of the course, including:
        - Course ID
        - Course name
        - List of enrolled student IDs
        - Instructor ID (if assigned)

        :returns: Dictionary containing serialized course data
        :rtype: dict
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "enrolled_students": [
                student.student_id for student in self.enrolled_students
            ],
            "instructor": self.instructor.instructor_id if self.instructor else None,
        }

    @classmethod
    def deserialize(cls, data, student_map, instructor_map):
        """
        Reconstruct a Course object from serialized data.

        Recreates a Course instance using provided serialization data
        and optional mappings for students and instructors.

        :param data: Serialized course data dictionary
        :type data: dict
        :param student_map: Mapping of student IDs to Student objects
        :type student_map: dict
        :param instructor_map: Mapping of instructor IDs to Instructor objects
        :type instructor_map: dict
        :returns: Reconstructed Course instance
        :rtype: Course
        """
        course = cls(data["course_id"], data["course_name"])
        if data["instructor"] is not None and len(instructor_map) > 0:
            course.instructor = instructor_map.get(data["instructor"])
        if len(student_map) > 0:
            course.enrolled_students = [
                student_map[student_id] for student_id in data["enrolled_students"]
            ]

        return course

    def __str__(self):
        """
        Provide a human-readable string representation of the Course.

        Generates a formatted string containing:
        - Course name
        - Instructor name (or 'None')
        - Enrolled students (or 'None')

        :returns: Formatted course description
        :rtype: str
        """
        instructor_name = self.instructor.name if self.instructor else "None"
        students = ", ".join(student.name for student in self.enrolled_students)
        return f"{self.course_name} (Instructor: {instructor_name}), Students: {students or 'None'})"

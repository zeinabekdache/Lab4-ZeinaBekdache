"""
Data Management Module

This module provides functionality for saving and loading school-related data
to and from JSON files, including students, instructors, and courses.
:module: data_management
"""

import json
from student import Student
from instructor import Instructor
from course import Course


class DataManagement:
    """
    A utility class for managing school data persistence.

    Provides static methods for serializing and deserializing
    school-related objects (students, instructors, courses)
    to and from JSON files.

    :method save_to_file: Saves school data to a JSON file
    :method load_from_file: Loads school data from a JSON file
    """

    @staticmethod
    def save_to_file(students, instructors, courses, file_name="school_data.json"):
        """
        Save school data to a JSON file.

        Serializes lists of students, instructors, and courses
        into a structured JSON file with indentation for readability.

        :param students: List of Student objects to be saved
        :type students: list of Student
        :param instructors: List of Instructor objects to be saved
        :type instructors: list of Instructor
        :param courses: List of Course objects to be saved
        :type courses: list of Course
        :param file_name: Name of the file to save data (default: "school_data.json")
        :type file_name: str, optional

        :return: None
        :raises IOError: If there's an issue writing to the file
        """
        data = {
            "students": [student.serialize() for student in students],
            "instructors": [instructor.serialize() for instructor in instructors],
            "courses": [course.serialize() for course in courses],
        }
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
            print(f"data saved to file {file_name}")

    @staticmethod
    def load_from_file(file_name="school_data.json"):
        """
        Load school data from a JSON file.

        Deserializes JSON data into Student, Instructor, and Course objects,
        reconstructing the relationships between them.

        :param file_name: Name of the file to load data from (default: "school_data.json")
        :type file_name: str, optional

        :return: Tuple containing lists of students, instructors, and courses
        :rtype: tuple(list of Student, list of Instructor, list of Course) or None

        :raises IOError: If there's an issue reading the file
        :raises json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                print(f"data loaded from file {file_name}")

                # Deserialize students, instructors, and courses with proper mapping
                student_map = {
                    s["student_id"]: Student.deserialize(s, {})
                    for s in data["students"]
                }
                instructor_map = {
                    i["instructor_id"]: Instructor.deserialize(i, {})
                    for i in data["instructors"]
                }
                course_map = {
                    c["course_id"]: Course.deserialize(c, student_map, instructor_map)
                    for c in data["courses"]
                }

                # Reconstruct student registered courses
                for student_data in data["students"]:
                    student = student_map[student_data["student_id"]]
                    student.registered_courses = [
                        course_map[course_id]
                        for course_id in student_data["registered_courses"]
                    ]

                # Reconstruct instructor assigned courses
                for instructor_data in data["instructors"]:
                    instructor = instructor_map[instructor_data["instructor_id"]]
                    instructor.assigned_courses = [
                        course_map[course_id]
                        for course_id in instructor_data["assigned_courses"]
                    ]

                return (
                    list(student_map.values()),
                    list(instructor_map.values()),
                    list(course_map.values()),
                )
        except Exception as e:
            print(e)
            return None

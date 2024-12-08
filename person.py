"""
Person Module

This module defines abstract Person class which can be inherited from to achieve polymorphic behavior
:module: person
"""

import re


class Person:
    """
    Represents a basic person with name, age, and email attributes.

    This class provides functionality for personal information management,
    including validation, email access, and serialization.

    :ivar name: Full name of the person
    :type name: str
    :ivar age: Age of the person
    :type age: int
    :ivar _Person__email: Private email address of the person
    :type _Person__email: str
    """

    def __init__(self, name, age, email):
        """
        Initialize a new Person instance.

        :param name: Full name of the person
        :type name: str
        :param age: Age of the person
        :type age: int
        :param email: Email address of the person
        :type email: str
        :raises ValueError: If name, age, or email is invalid
        """
        self.name = name
        self.age = age
        self.__email = email
        self.validate()

    def introduce(self):
        """
        Print a friendly introduction of the person.

        Outputs a string with name, age, and email information.

        :returns: None
        :rtype: None
        """
        print(
            f"Hi, I'm {self.name}, and I am {self.age} years old. My email is {self.__email}."
        )

    def get_email(self):
        """
        Retrieve the person's email address.

        :returns: Email address
        :rtype: str
        """
        return self.__email

    def set_email(self, new_email):
        """
        Update the person's email address.

        :param new_email: New email address to set
        :type new_email: str
        :raises ValueError: If the new email is not in a valid format
        """
        self.__email = new_email
        self.validate_email()

    def validate_name(self):
        """
        Validate the person's name.

        Checks that the name is at least two characters long after stripping whitespace.

        :raises ValueError: If name is less than two characters long
        """
        if len(self.name.strip()) < 2:
            raise ValueError("name must have at least two characters.")

    def validate_email(self):
        """
        Validate the email address format.

        Uses a simple regex pattern to check email validity.

        :raises ValueError: If email does not match the expected format
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.__email):
            raise ValueError("Invalid email format")

    def validate_age(self):
        """
        Validate the person's age.

        Ensures the age is a positive number.

        :raises ValueError: If age is zero or negative
        """
        if self.age <= 0:
            raise ValueError("Age cannot be negative or zero")

    def validate(self):
        """
        Perform comprehensive validation of person's attributes.

        Calls individual validation methods for email, age, and name.

        :raises ValueError: If any validation check fails
        """
        self.validate_email()
        self.validate_age()
        self.validate_name()

    def serialize(self):
        """
        Convert person's information to a serializable dictionary.

        :returns: Dictionary containing person's attributes
        :rtype: dict
        """
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email,
            "type": self.__class__.__name__,
        }

    @classmethod
    def deserialize(cls, data):
        """
        Reconstruct a Person instance from serialized data.

        :param data: Dictionary containing person's serialized information
        :type data: dict
        :returns: Reconstructed Person instance
        :rtype: Person
        """
        return cls(data["name"], data["age"], data["email"])

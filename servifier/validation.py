"""
Provide some basic descriptors for validating requests to API.

Author: Nikolay Lysenko
"""


import datetime
from abc import ABCMeta, abstractmethod
from typing import Any
from weakref import WeakKeyDictionary


class BaseField:
    """Abstract descriptor representing a field of POST request."""

    __metaclass__ = ABCMeta

    def __init__(self, required: bool):
        """
        Initialize an instance.

        :param required:
            if it is `True`, field value must be passed explicitly
        """
        self.data = WeakKeyDictionary()
        self.required = required

    def __get__(self, instance: Any, owner: Any) -> Any:
        """Get value."""
        value = self.data.get(instance)
        return value

    @abstractmethod
    def __set__(self, instance: Any, value: Any) -> None:
        """Check that a value is in accordance with instance settings."""
        if value is None and self.required:
            raise ValueError("Required fields must be passed explicitly.")


class BaseTypedField(BaseField):
    """
    Abstract descriptor representing a field that must have a particular type.
    """

    field_type = type(None)

    def __set__(self, instance: Any, value: Any) -> None:
        """Check that a value is in accordance with instance settings."""
        super().__set__(instance, value)
        if value is not None and not isinstance(value, self.field_type):
            raise ValueError(
                f"Value {value} has type {type(value)}, "
                f"but {self.field_type} was expected."
            )
        self.data[instance] = value


class StringField(BaseTypedField):
    """Descriptor that prohibits non-string values."""

    field_type = str


class IntegerField(BaseTypedField):
    """Descriptor that prohibits non-integer values."""

    field_type = int


class FloatField(BaseTypedField):
    """Descriptor that prohibits non-float values."""

    field_type = float


class StandardDateField(StringField):
    """Descriptor that permits only dates in 'YYYY-MM-DD' format."""

    def __set__(self, instance: Any, value: Any):
        super().__set__(instance, value)
        if value:
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Date {value} is not in format 'YYYY-MM-DD'")
            self.data[instance] = value

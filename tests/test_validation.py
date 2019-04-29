"""
Test `servifier.validation` module.

Author: Nikolay Lysenko
"""


import pytest

from servifier import validation


class DescriptorMock(object):
    """Mock for a class that has fields with descriptors."""

    def __init__(self, value):
        self.value = value


def test_string_field_with_non_string() -> None:
    """Test `StringField` descriptor with integer value."""
    DescriptorMock.value = validation.StringField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(1)
    assert "<class 'str'> was expected" in str(exc_info.value)


def test_string_field_with_valid_values():
    """Test `CharField` descriptor with valid strings."""
    DescriptorMock.value = validation.StringField(required=True)
    DescriptorMock("a")
    DescriptorMock("A + b")


def test_integer_field_with_non_integer():
    """Test `IntegerField` descriptor with float value."""
    DescriptorMock.value = validation.IntegerField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(1.0)
    assert "<class 'int'> was expected" in str(exc_info.value)


def test_integer_field_with_valid_values():
    """Test `IntegerField` descriptor with valid integers."""
    DescriptorMock.value = validation.IntegerField(required=True)
    DescriptorMock(1)
    DescriptorMock(-999)


def test_float_field_with_non_float():
    """Test `FloatField` descriptor with integer value."""
    DescriptorMock.value = validation.FloatField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(1)
    assert "<class 'float'> was expected" in str(exc_info.value)


def test_float_field_with_valid_values():
    """Test `FloatField` descriptor with valid floats."""
    DescriptorMock.value = validation.FloatField(required=True)
    DescriptorMock(1.0)
    DescriptorMock(-999.5)


def test_standard_date_field_with_wrong_format():
    """Test `StandardDateField` descriptor with wrong format."""
    DescriptorMock.value = validation.StandardDateField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock("1990.01.01")
    assert 'is not in format' in str(exc_info.value)


def test_standard_date_field_with_valid_values():
    """Test `StandardDateField` descriptor with valid dates."""
    DescriptorMock.value = validation.StandardDateField(required=True)
    DescriptorMock("1990-01-01")
    DescriptorMock("1890-12-30")

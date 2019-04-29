"""
Test `servifier.validation` module.

Author: Nikolay Lysenko
"""


from typing import Any

import pytest

from servifier import validation


class DescriptorMock(object):
    """Mock for a class that has fields with descriptors."""

    def __init__(self, value):
        self.value = value


@pytest.mark.parametrize(
    "value", [1, []]
)
def test_string_field_with_non_string(value: Any) -> None:
    """Test `StringField` descriptor with integer value."""
    DescriptorMock.value = validation.StringField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(value)
    assert "<class 'str'> was expected" in str(exc_info.value)


@pytest.mark.parametrize(
    "value", ['a', 'A + b']
)
def test_string_field_with_valid_values(value: Any) -> None:
    """Test `CharField` descriptor with valid strings."""
    DescriptorMock.value = validation.StringField(required=True)
    descriptor_mock = DescriptorMock(value)
    assert descriptor_mock.value == value


@pytest.mark.parametrize(
    "value", ['a', 1.0]
)
def test_integer_field_with_non_integer(value: Any) -> None:
    """Test `IntegerField` descriptor with float value."""
    DescriptorMock.value = validation.IntegerField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(value)
    assert "<class 'int'> was expected" in str(exc_info.value)


@pytest.mark.parametrize(
    "value", [1, -999]
)
def test_integer_field_with_valid_values(value: Any) -> None:
    """Test `IntegerField` descriptor with valid integers."""
    DescriptorMock.value = validation.IntegerField(required=True)
    descriptor_mock = DescriptorMock(value)
    assert descriptor_mock.value == value


@pytest.mark.parametrize(
    "value", [[1.0], 'a']
)
def test_float_field_with_non_float(value: Any) -> None:
    """Test `FloatField` descriptor with integer value."""
    DescriptorMock.value = validation.FloatField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(value)
    assert "<class 'float'> was expected" in str(exc_info.value)


@pytest.mark.parametrize(
    "value", [1.0, -999.5]
)
def test_float_field_with_valid_values(value: Any) -> None:
    """Test `FloatField` descriptor with valid floats."""
    DescriptorMock.value = validation.FloatField(required=True)
    descriptor_mock = DescriptorMock(value)
    assert descriptor_mock.value == value


@pytest.mark.parametrize(
    "value", ['1990.01.01', '2000-02-31']
)
def test_standard_date_field_with_wrong_format(value: Any) -> None:
    """Test `StandardDateField` descriptor with wrong format."""
    DescriptorMock.value = validation.StandardDateField(required=True)
    with pytest.raises(ValueError) as exc_info:
        DescriptorMock(value)
    assert 'is not in format' in str(exc_info.value)


@pytest.mark.parametrize(
    "value", ['1990-01-01', '1890-12-30']
)
def test_standard_date_field_with_valid_values(value: Any) -> None:
    """Test `StandardDateField` descriptor with valid dates."""
    DescriptorMock.value = validation.StandardDateField(required=True)
    descriptor_mock = DescriptorMock(value)
    assert descriptor_mock.value == value


def test_standard_date_field_which_is_optional() -> None:
    """Test `StandardDateField` descriptor with `None`."""
    DescriptorMock.value = validation.StandardDateField(required=False)
    descriptor_mock = DescriptorMock(None)
    assert descriptor_mock.value is None

"""
Create global fixtures.

Author: Nikolay Lysenko
"""


from typing import Dict, Any

import pytest
from flask.testing import FlaskClient

from servifier import HandleSpec, create_app, validation
from servifier.auth import generate_token


def evaluate_apartment(area: float, distance_to_underground: int) -> float:
    """Estimate price of an apartment."""
    price = 200000 * area - 1000 * distance_to_underground
    return price


class ApartmentParameters:
    """Parameters of an apartment"""

    area = validation.FloatField(required=True)
    distance_to_underground = validation.IntegerField(required=True)

    def __init__(self, area: float, distance_to_underground: int):
        self.area = area
        self.distance_to_underground = distance_to_underground


@pytest.fixture()
def apartment_prices_app_client() -> FlaskClient:
    """Create client for demo Flask app that evaluates apartments."""
    handle_spec = HandleSpec(
        evaluate_apartment,
        '/evaluate',
        ApartmentParameters,
        '1234'
    )
    app = create_app([handle_spec])
    client = app.test_client()
    yield client


@pytest.fixture()
def sample_apartment_prices_request() -> Dict[str, Any]:
    """Create a valid request to apartment evaluation API."""
    login = 'user'
    token = generate_token(login, auth_salt='1234')
    request = {
        'login': login,
        'token': token,
        'area': 68.5,
        'distance_to_underground': 300
    }
    return request


def failing_func(first: int, second: int) -> None:
    """Fail."""
    raise ValueError('{} {}'.format(first, second))


@pytest.fixture()
def simple_broken_app_client() -> FlaskClient:
    """Create client for demo Flask app that fails internally."""
    handle_spec = HandleSpec(
        failing_func,
        '/fail'
    )
    app = create_app([handle_spec])
    client = app.test_client()
    yield client

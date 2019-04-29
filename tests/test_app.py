"""
Test behavior of Flask app created by `app_factory`.

Author: Nikolay Lysenko
"""


import json
from typing import Dict, Any

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "area, distance_to_underground, expected",
    [
        (30.0, 300, 5700000),
        (65.5, 1000, 12100000),
        (99.0, 100, 19700000)
    ]
)
def test_valid_requests(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any],
        area: float, distance_to_underground: int, expected: float
) -> None:
    """Test that app properly responds to valid requests."""
    arguments = {
        "area": area, "distance_to_underground": distance_to_underground
    }
    request = {**sample_apartment_prices_request, **arguments}
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(request),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json['result'] == expected


def test_request_to_absent_handle(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app informs users about non-existing handles."""
    response = apartment_prices_app_client.post(
        '/non_existing_handle',
        data=json.dumps(sample_apartment_prices_request),
        content_type='application/json'
    )
    assert response.status_code == 404
    assert 'Not Found' in response.json['error']


def test_bad_request_without_json(
        apartment_prices_app_client: FlaskClient
) -> None:
    """Test that app reports about requests without JSON attachment."""
    response = apartment_prices_app_client.post(
        '/evaluate'
    )
    assert response.status_code == 400
    assert 'Bad Request' in response.json['error']


def test_bad_request_with_empty_json(
        apartment_prices_app_client: FlaskClient
) -> None:
    """Test that app reports about requests with empty JSON."""
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'Bad Request' in response.json['error']


def test_bad_request_with_broken_json(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app reports about requests of bad structure."""
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(sample_apartment_prices_request)[:-1],
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'Bad Request' in response.json['error']


def test_unauthorized_request_with_no_credentials(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app forbids requests without login and token."""
    sample_apartment_prices_request.pop('login')
    sample_apartment_prices_request.pop('token')
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(sample_apartment_prices_request),
        content_type='application/json'
    )
    assert response.status_code == 403
    assert 'Forbidden' in response.json['error']


def test_unauthorized_request_with_wrong_token(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app forbids requests with wrong token."""
    sample_apartment_prices_request["token"] = '123'
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(sample_apartment_prices_request),
        content_type='application/json'
    )
    assert response.status_code == 403
    assert 'Forbidden' in response.json['error']


def test_invalid_request_with_less_fields(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app reports about requests with some fields missed."""
    sample_apartment_prices_request.pop('area')
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(sample_apartment_prices_request),
        content_type='application/json'
    )
    assert response.status_code == 422
    assert 'Invalid Request' in response.json['error']


def test_invalid_request_with_wrong_types(
        apartment_prices_app_client: FlaskClient,
        sample_apartment_prices_request: Dict[str, Any]
) -> None:
    """Test that app reports about requests with invalid data."""
    sample_apartment_prices_request['area'] = 68
    response = apartment_prices_app_client.post(
        '/evaluate',
        data=json.dumps(sample_apartment_prices_request),
        content_type='application/json'
    )
    assert response.status_code == 422
    assert 'Invalid Request' in response.json['error']


def test_internal_server_errors(simple_broken_app_client: FlaskClient) -> None:
    """Test that app reports about internal server errors."""
    response = simple_broken_app_client.post(
        '/fail',
        data=json.dumps({'a': 1}),
        content_type='application/json'
    )
    assert response.status_code == 500
    assert 'Internal Server Error' in response.json['error']

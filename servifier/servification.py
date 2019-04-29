"""
Modify a Python function in order to make it a part of API.

Author: Nikolay Lysenko
"""


import logging
from typing import Tuple, Dict, Callable, Optional, Any

from flask import request, jsonify

from servifier import constants
from servifier.auth import check_auth
from servifier.utils import report_error


def get_request_data() -> Tuple[Optional[Dict[str, Any]], bool]:
    """Get data from JSON contained by request."""
    try:
        data = request.get_json()
        return data, False
    except:
        logging.exception('Can not parse JSON: ')
        return None, True


def validate_request_data(
        data: Dict[str, Any], validator_class: Optional[type]
) -> bool:
    """Validate input parameters from user request."""
    if validator_class is None:
        return False
    try:
        _ = validator_class(**data)
        return False
    except TypeError:
        logging.exception('Wrong number of arguments: ')
        return True
    except:
        logging.exception('Arguments validation failed: ')
        return True


def run_function(func: Callable, inputs: Dict[str, Any]) -> Tuple[Any, bool]:
    """Run Python function with requested inputs."""
    try:
        result = func(**inputs)
        return result, False
    except:
        logging.exception('Unexpected internal error: ')
        return None, True


def servify(handle_spec: 'servifier.HandleSpec') -> Callable:
    """Prepare Python function for being a part of API."""

    def wrapped() -> Tuple[str, int]:
        data, any_errors = get_request_data()
        if any_errors:
            return report_error('can not parse JSON', constants.BAD_REQUEST)
        if not data:
            return report_error('empty JSON', constants.BAD_REQUEST)

        allowed = check_auth(data, handle_spec.auth_salt)
        if not allowed:
            return report_error('check login and token', constants.FORBIDDEN)
        if handle_spec.auth_salt is not None:
            data.pop('login')
            data.pop('token')

        any_errors = validate_request_data(data, handle_spec.validator_class)
        if any_errors:
            return report_error('check your JSON', constants.INVALID_REQUEST)

        result, any_errors = run_function(handle_spec.func, data)
        if any_errors:
            return report_error('something failed', constants.INTERNAL_ERROR)

        response = {'result': result, 'status': constants.OK}
        return jsonify(response), constants.OK

    func_name = handle_spec.path.replace('/', '_')
    wrapped.__name__ = func_name  # Names of such functions must be unique.
    return wrapped

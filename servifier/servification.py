"""
Modify a Python function in order to make it a part of API.

Author: Nikolay Lysenko
"""


import logging
from typing import Tuple, Dict, Callable, Optional, Any

from flask import request, jsonify

from servifier import constants


def report_error(msg: str, status: int) -> Tuple[str, int]:
    """Report error (it is just a helper function for repetitive pieces)."""
    response_data = {
        'error': f'{constants.ERRORS[status]}: {msg}',
        'status': status
    }
    return jsonify(response_data), status


def get_request_data() -> Tuple[Optional[Dict[str, Any]], bool]:
    """Get data from JSON contained by request."""
    try:
        request_data = request.get_json()
        return request_data, False
    except:
        logging.exception('Can not parse JSON: ')
        return None, True


def run_function(func: Callable, inputs: Dict[str, Any]) -> Tuple[Any, bool]:
    """Run Python function with requested inputs."""
    try:
        result = func(**inputs)
        return result, False
    except:
        logging.exception('Unexpected internal error: ')
        return None, True


def servify(func: Callable, name: str) -> Callable:
    """Prepare Python function for being a part of API."""

    def wrapped() -> Tuple[str, int]:
        request_data, any_exceptions = get_request_data()
        if any_exceptions:
            return report_error('can not parse JSON', constants.BAD_REQUEST)
        if request_data is None:
            return report_error('empty JSON', constants.BAD_REQUEST)

        result, any_exceptions = run_function(func, request_data)
        if any_exceptions:
            return report_error('something failed', constants.INTERNAL_ERROR)

        response_data = {'result': result, 'status': constants.OK}
        return jsonify(response_data), constants.OK

    wrapped.__name__ = name  # Names of such functions must be unique.
    return wrapped

"""
Modify a Python function in order to make it a part of API.

Author: Nikolay Lysenko
"""


import logging
from typing import Tuple, Callable

from flask import request, jsonify

from servifier import constants


def report_error(msg: str, status: int) -> Tuple[str, int]:
    """Report error (it is just a helper function for repetitive pieces)."""
    response_data = {
        'error': f'{constants.ERRORS[status]}: {msg}',
        'status': status
    }
    return jsonify(response_data), status


def servify(func: Callable, name: str) -> Callable:
    """Prepare Python function for being a part of API."""

    def wrapped() -> Tuple[str, int]:
        # Check that JSON can be extracted and parsed.
        try:
            request_data = request.get_json()
        except:
            logging.exception('Can not parse JSON: ')
            return report_error('can not parse JSON', constants.BAD_REQUEST)

        # Check that JSON is not empty.
        if request_data is None:
            return report_error('empty JSON', constants.BAD_REQUEST)

        # Invoke Python function.
        try:
            response = func(**request_data)
        except:
            logging.exception('Unexpected internal error: ')
            return report_error('something failed', constants.INTERNAL_ERROR)

        response_data = {'response': response, 'status': constants.OK}
        return jsonify(response_data), constants.OK

    wrapped.__name__ = name  # Names of such functions must be unique.
    return wrapped

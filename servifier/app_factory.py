"""
Create Flask app based on user-defined specifications.

Author: Nikolay Lysenko
"""


import logging
from typing import List, Tuple, Callable, Optional

from flask import Flask, request, jsonify

from servifier import constants
from servifier.validation import Validator


class HandleSpec:
    """Represent specifications of an API handle."""

    def __init__(
            self, func: Callable, path: str,
            validator: Optional[Validator] = None
    ):
        """
        Initialize an instance.

        :param func:
            Python function that should respond to request to this handle
        :param path:
            API path (from root) to this handle
        :param validator:
            instance that validates data from requests
        """
        self.func = func
        self.path = path
        self.validator = validator


def report_error(msg: str, status: int) -> Tuple[str, int]:
    """Report error."""
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


def create_app(specs: List[HandleSpec]) -> Flask:
    """Create Flask app based on passed specifications."""
    app = Flask(__name__)
    for handle_spec in specs:
        func_name = handle_spec.path.replace('/', '_')
        servified_func = servify(handle_spec.func, func_name)
        app.route(handle_spec.path, methods=['POST'])(servified_func)
    return app

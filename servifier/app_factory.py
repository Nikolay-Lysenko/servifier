"""
Create Flask app based on user-defined specifications.

Author: Nikolay Lysenko
"""


from collections import namedtuple
from typing import List

from flask import Flask

from servifier import constants
from servifier.servification import servify, report_error


HandleSpec = namedtuple('HandleSpec', ['func', 'path', 'validator'])
HandleSpec.__new__.__defaults__ = (None,)  # NB: It is syntax for Python < 3.7.
HandleSpec.__doc__ = (
    '''
    Specification of an API handle.
    
    :param func:
        Python function that should respond to request to this handle
    :param path:
        API path (from root) to this handle
    :param validator:
        (optional) instance of `servifier.validation.Validator`
        for checking fields of a request
    '''
)


def create_app(specs: List[HandleSpec]) -> Flask:
    """Create Flask app based on passed specifications."""
    app = Flask(__name__)
    for handle_spec in specs:
        func_name = handle_spec.path.replace('/', '_')
        servified_func = servify(handle_spec.func, func_name)
        app.route(handle_spec.path, methods=['POST'])(servified_func)
    app.errorhandler(constants.NOT_FOUND)(
        lambda _: report_error('no such handle', constants.NOT_FOUND)
    )
    return app

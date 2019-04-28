"""
Create Flask app based on user-defined specifications.

Author: Nikolay Lysenko
"""


from collections import namedtuple
from typing import List

from flask import Flask

from servifier import constants
from servifier.servification import servify
from servifier.utils import report_error


HandleSpec = namedtuple(
    'HandleSpec',
    ['func', 'path', 'validator_class', 'auth_salt']
)
HandleSpec.__new__.__defaults__ = (None, None)  # NB: It's Python < 3.7 syntax.
HandleSpec.__doc__ = (
    '''
    Specification of an API handle.
    
    :param func:
        Python function that should respond to request to this handle
    :param path:
        API path (from root) to this handle
    :param validator_class:
        (optional) user-defined class such that its arguments are
        exactly the same as arguments of `func` and descriptors are
        provided for all of them
    :param auth_salt:
        (optional) if it is not passed, there is no authentication;
        if a string is passed as this argument, requests must include
        'login' and 'token' fields where valid value of 'token' depends on
        value of 'login' and this salt
    '''
)


def create_app(specs: List[HandleSpec]) -> Flask:
    """Create Flask app based on passed specifications."""
    app = Flask(__name__)
    for handle_spec in specs:
        servified_func = servify(handle_spec)
        app.route(handle_spec.path, methods=['POST'])(servified_func)
    app.errorhandler(constants.NOT_FOUND)(
        lambda _: report_error('check handle address', constants.NOT_FOUND)
    )
    return app

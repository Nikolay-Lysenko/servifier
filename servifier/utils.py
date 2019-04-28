"""
Do supplementary things.

Author: Nikolay Lysenko
"""


from typing import Tuple

from flask import jsonify

from servifier import constants


def report_error(msg: str, status: int) -> Tuple[str, int]:
    """Report error (it is just a helper function for repetitive pieces)."""
    response_data = {
        'error': f'{constants.ERRORS[status]}: {msg}',
        'status': status
    }
    return jsonify(response_data), status

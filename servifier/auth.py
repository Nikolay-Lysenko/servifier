"""
Authenticate requests by login and token.

Author: Nikolay Lysenko
"""


import hashlib
import logging
from typing import Dict, Optional, Any


def generate_token(login: str, auth_salt: str) -> str:
    """Generate token based on login and hash salt."""
    encoded_key = (login + auth_salt).encode('utf-8')
    token = hashlib.sha512(encoded_key).hexdigest()
    return token


def check_auth(data: Dict[str, Any], auth_salt: Optional[str]) -> bool:
    """Check that request is properly authorized."""
    if auth_salt is None:
        return True
    try:
        expected_token = generate_token(data['login'], auth_salt)
        return data['token'] == expected_token
    except:
        logging.exception('Malformed request: ')
        return False

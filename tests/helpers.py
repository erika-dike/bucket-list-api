"""
Contains functions that test_files use
"""
from base64 import b64encode


def create_api_headers(username, password):
    return {
        'Authorization':
            'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).
            decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
    }

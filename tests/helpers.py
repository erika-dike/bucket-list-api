"""
Contains functions that test_files use
"""
import json
from base64 import b64encode
from flask import url_for


def create_api_headers(username, password):
    return {
        'Authorization':
            'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).
            decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
    }

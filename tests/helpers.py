"""
Contains functions that test_files use
"""
from base64 import b64encode


def create_api_headers(username_or_token, password):
    print username_or_token
    if password == '':
        auth_type = 'Token ' + username_or_token
        print auth_type
    else:
        auth_type = 'Basic ' + b64encode((username_or_token + ':' +
            password).encode('utf-8')).decode('utf-8')

    return {
        'Authorization': auth_type,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

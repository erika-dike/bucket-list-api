from flask import g
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth
from .models import User
from .errors import unauthorized

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')


@basic_auth.verify_password
def verify_password(username, password):
    """Verifies login credentials supplied are valid"""
    # first try to authenticate by token
    # try to authenticate with username/password
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    """Verifies that token supplied is valid"""
    if token == '':
        return False
    user = User.verify_auth_token(token)
    g.user = user
    return True


@token_auth.error_handler
def unauthorized_error():
    return unauthorized('Please authenticate to access this API')

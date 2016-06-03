from flask import g, jsonify, request

from api_init import api
from ..auth import auth, verify_password
from ..decorators import json
from .. import errors
from ..models import db, User


@api.route('/auth/login', methods=['POST'])
@json
def login():
    """Logins in a user and returns an authentication token"""
    username = request.json.get('username')
    password = request.json.get('password')

    if verify_password(username, password):
        return {'token': g.user.generate_auth_token()}
    else:
        return errors.unauthorized('Your login credentials are incorrect')


@api.route('/auth/register', methods=['POST'])
@json
def register():
    """Creates a new user and saves user to database"""
    username = request.json.get('username')
    password = request.json.get('password')
    if username in [None, "", " "]:
        return errors.bad_request("You must provide a username")
    if password is None or len(password) < 6:
        return errors.bad_request("Password must be no less than 6 characters")
    if User.query.filter_by(username=username).first() is not None:
        return errors.bad_request("That username is already taken")
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user, 201, {'Location': user.get_url()}


@api.route('/users/<int:id>', methods=['GET'])
@json
def get_user(id):
    """Returns a user"""
    return User.query.get_or_404(id)

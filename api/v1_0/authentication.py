from flask import g, jsonify, request, url_for

from api import api
from ..auth import auth
from ..decorators import json
from ..models import db, User
import errors


@api.route('/auth/login', methods=['GET'])
@auth.login_required
@json
def login():
    return {'token': g.user.generate_auth_token()}


@api.route('/auth/register', methods=['POST'])
# @json
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    # user = User().from_json(request.json)
    if username is None or password is None:
        errors.bad_request(400)
    if User.query.filter_by(username=username).first() is not None:
        errors.bad_request(400)  # existing user
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user, 201, {'Location': user.get_url()}


@api.route('/users/<int:id>', methods=['GET'])
@json
def get_user(id):
    return User.query.get_or_404(id)


@api.route('/auth/hello')
def index():
    return "hello, world!"
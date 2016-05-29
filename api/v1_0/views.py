from flask import url_for, request

from ..auth import auth
from api import api
from ..decorators import json
from ..models import db, User


@api.route('/bucketlists')
@auth.login_required
def bucketlists():
    return "hello, world!"

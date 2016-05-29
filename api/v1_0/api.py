from flask import Blueprint, g

api = Blueprint('api', __name__)

# do this last to avoid circular dependencies
from . import authentication, views
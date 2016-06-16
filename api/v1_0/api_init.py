from flask import Blueprint
from ..errors import ValidationError, bad_request, not_found

api = Blueprint('api', __name__)


@api.errorhandler(ValidationError)
def validation_error(error):
    return bad_request(error.args[0])


@api.errorhandler(404)
def not_found_error(error):
    return not_found('item not found')


# do this last to avoid circular dependencies
from . import authentication, views

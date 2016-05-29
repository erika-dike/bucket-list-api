from flask import jsonify


class ValidationError(ValueError):
    pass


def unauthorized(message):
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response

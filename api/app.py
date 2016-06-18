from flask import Flask, jsonify
from flask.ext.compress import Compress
from werkzeug.exceptions import default_exceptions, HTTPException

from .models import db
from config import config

# initialize compress
compress = Compress()


def create_app(config_name, **kwargs):
    """
    Creates a compressed JSON-oriented Flask app

    All error responses not specifically managed will have
    application/json content type, and will contain JSON.

    courtesy - Pavel Repin (code for returning JSON errors)
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(__name__, **kwargs)
    app.config.from_object(config[config_name])

    # pass flask object to compress object
    compress.init_app(app)

    # pass flask object to db object
    db.init_app(app)

    # register base route
    from api.v1_0.api_init import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

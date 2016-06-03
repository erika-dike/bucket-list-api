import os

from flask import Flask
from flask.ext.compress import Compress

from .models import db
from config import config

# initialize compress
compress = Compress()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # pass flask object to compress object
    compress.init_app(app)

    # pass flask object to db object
    db.init_app(app)

    # register base route
    from api.v1_0.api_init import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app

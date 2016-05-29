import os

from flask import Flask

from .models import db
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from api.v1_0.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app

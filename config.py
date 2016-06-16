"""
Settings for the Bucket List API
"""


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'that_uyona_boy_wanna_do_good'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'bucketlistdb.sqlite')
    USE_TOKEN_AUTH = True
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'bucketlistdb-test.sqlite')
    SERVER_NAME = 'localhost:5000'


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

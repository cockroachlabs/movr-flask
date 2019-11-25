# This file defines classes for flask configuration
import os

class Config(object):
    DEBUG = True
    TESTING = True
    ENV = 'development'
    SECRET_KEY = os.urandom(16)


class DevConfig(Config):
    DEBUG = os.environ['DEBUG']
    SECRET_KEY = os.environ['SECRET_KEY']
    API_KEY = os.environ['API_KEY']
    DB_URI = os.environ['DB_URI']

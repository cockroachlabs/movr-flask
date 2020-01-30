# This file defines classes for flask configuration
import os


class Config:
    """Flask configuration class.
    """
    DEBUG = os.environ['DEBUG']
    SECRET_KEY = os.environ['SECRET_KEY']
    API_KEY = os.environ['API_KEY']
    DB_URI = os.environ['DB_URI']
    PREFERRED_URL_SCHEME = ('https', 'http')[DEBUG == 'True']

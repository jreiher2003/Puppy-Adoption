import os
import secret_key

# default config
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = secret_key.secret_key
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    # print SQLALCHEMY_DATABASE_URI
   

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # print SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # print SQLALCHEMY_DATABASE_URI


class ProductionConfig(BaseConfig):
    DEBUG = False
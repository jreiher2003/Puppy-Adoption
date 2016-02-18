import os


# default config
class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    ACCOUNT_SID = os.environ['ACCOUNT_SID']
    AUTH_TOKEN = os.environ['AUTH_TOKEN']
    # print SQLALCHEMY_DATABASE_URI
   

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # print SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # print SQLALCHEMY_DATABASE_URI


class ProductionConfig(BaseConfig):
    DEBUG = False
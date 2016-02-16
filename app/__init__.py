import os
from flask import Flask 
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS'])

mail = Mail(app)
db = SQLAlchemy(app)

from app import views, models
from models import *
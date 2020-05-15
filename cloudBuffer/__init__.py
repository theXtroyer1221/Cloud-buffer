from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_whooshalchemy as wa
from flask_whooshee import Whooshee
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask

import json
import requests
import os

from dotenv import load_dotenv
load_dotenv()

#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

whooshee = Whooshee(app)
app.config["WHOOSH_BASE"] = "whoosh"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)

from cloudBuffer import routes
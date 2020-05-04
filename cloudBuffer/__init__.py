from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import json
import requests

from dotenv import load_dotenv
load_dotenv()

from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from cloudBuffer import routes
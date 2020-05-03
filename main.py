from flask import Flask, render_template, request, redirect, url_for, flash
from forms import SearchForm, locationSearch, RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

import json
import requests
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

import os

from google_images_search import GoogleImagesSearch

from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["TEMPLATES_AUTO_RELOAD"] = True

GCS_DEVELOPER_KEY = os.environ.get('GCS_DEVELOPER_KEY')
GCS_CX = os.environ.get('GCS_CX')
IP_STACK = os.environ.get("IP_STACK")

app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    location_form = locationSearch()

    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    if request.args.get("hfield", None):
        headers_list = request.headers.getlist("X-Forwarded-For")
        user_ip = headers_list[0] if headers_list else request.remote_addr
        url = 'http://api.ipstack.com/{}?access_key={}'.format(
            "83.250.184.69", IP_STACK)
        r = requests.get(url)
        j = r.json()
        query = j["city"]

        return redirect(url_for("search", query=query))

    return render_template("index.html",
                           form=form,
                           location_form=location_form,
                           data="data")


@app.route("/weather/<query>")
def search(query):
    form = SearchForm()
    location_form = locationSearch()

    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    if request.args.get("hfield", None):
        headers_list = request.headers.getlist("X-Forwarded-For")
        user_ip = headers_list[0] if headers_list else request.remote_addr
        url = 'http://api.ipstack.com/{}?access_key={}'.format(
            "83.250.184.69", IP_STACK)
        r = requests.get(url)
        j = r.json()
        query = j["city"]

        return redirect(url_for("search", query=query))

    payload = {
        'q': query,
        'units': 'metric',
        'appid': 'd4783db24d0d806b60afb366ceea4d7e'
    }
    r = requests.get('http://api.openweathermap.org/data/2.5/weather',
                     params=payload)
    data = r.json()

    if data["cod"] == 200:
        search_country = data["sys"]["country"]
        search_query = f"{query} city {search_country}"

        gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
        google_search_params = {
            'q': search_query,
            'num': 1,
            'safe': 'off',
            'imgSize': 'xlarge'
        }
        try:
            gis.search(search_params=google_search_params)
        except:
            img = "../static/images/notfound.jpg"

        img = "../static/images/notfound.jpg"

        for image in gis.results():
            img = image.url

        return render_template("search.html",
                               query=query,
                               data=data,
                               form=form,
                               location_form=location_form,
                               img=img)
    else:
        return render_template("search.html",
                               query=query,
                               data=data,
                               form=form,
                               location_form=location_form)


@app.route("/blog")
def blog():
    return render_template("blog.html", data="data", title="Blog")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('blog'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')

    return render_template("login.html",
                           form=form,
                           data="data",
                           title="Log in")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('blog'))

    return render_template("signup.html",
                           form=form,
                           data="data",
                           title="Sign up")


@app.errorhandler(404)
def page_not_found(e):
    data = "error"
    return render_template('error.html', e=e, data=data), 404


if __name__ == "__main__":
    app.run(debug=True)
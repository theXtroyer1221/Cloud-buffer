from cloudBuffer.forms import SearchForm, locationSearch, RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from cloudBuffer.models import User, Post
from cloudBuffer import app, bcrypt, db, login_manager

import requests
import os
import secrets

from google_images_search import GoogleImagesSearch

GCS_DEVELOPER_KEY = os.environ.get('GCS_DEVELOPER_KEY')
GCS_CX = os.environ.get('GCS_CX')
IP_STACK = os.environ.get("IP_STACK")


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        logout_user()
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
    if current_user.is_authenticated:
        logout_user()
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
    if current_user.is_authenticated:
        image_file = url_for("static",
                             filename="profile_pics/" +
                             current_user.image_file)
    return render_template("blog.html", data="data", title="Blog")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(
                url_for("blog"))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')

    return render_template("login.html",
                           form=form,
                           data="data",
                           title="Log in")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Your account has been created, you are now able to log in, {form.username.data}',
            'success')
        return redirect(url_for('login'))

    return render_template("signup.html",
                           form=form,
                           data="data",
                           title="Sign up")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics",
                                picture_fn)
    form_picture.save(picture_path)

    return picture_fn
    #hello


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account information has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template("account.html",
                           title="Account",
                           image_file=image_file,
                           form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("blog"))


@app.errorhandler(404)
def page_not_found(e):
    data = "error"
    return render_template('error.html', e=e, data=data), 404
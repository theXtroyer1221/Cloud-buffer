from flask import Flask, render_template, request, redirect, url_for
from forms import SignUpForm

import json
import requests

from dotenv import load_dotenv
load_dotenv()

import os

from google_images_search import GoogleImagesSearch

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["TEMPLATES_AUTO_RELOAD"] = True

GCS_DEVELOPER_KEY = os.environ.get('GCS_DEVELOPER_KEY')
GCS_CX = os.environ.get('GCS_CX')


@app.route("/", methods=["GET", "POST"])
def index():
    form = SignUpForm()
    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    return render_template("index.html", form=form, data="data")


@app.route("/weather/<query>")
def search(query):
    form = SignUpForm()

    if request.args.get("search", None):
        query = request.args["search"]

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
            'fileType': 'jpg',
            'imgSize': 'xlarge'
        }
        try:
            gis.search(search_params=google_search_param)
        except:
            img = "../static/images/notfound.jpg"

        img = "../static/images/notfound.jpg"

        for image in gis.results():
            img = image.url

        return render_template("search.html",
                               query=query,
                               data=data,
                               form=form,
                               img=img)
    else:
        return render_template(
            "search.html",
            query=query,
            data=data,
            form=form,
        )


@app.errorhandler(404)
def page_not_found(e):
    data = "error"
    return render_template('error.html', e=e, data=data), 404


@app.route("/")
def lolol():
    data = request.get_json()
    return data


if __name__ == "__main__":
    app.run(debug=True)
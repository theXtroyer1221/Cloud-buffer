from flask import Flask, render_template, request, redirect, url_for
from forms import SignUpForm

import json
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    form = SignUpForm()
    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    return render_template("index.html", form=form)


@app.route("/<query>")
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

    return render_template("search.html", query=query, data=data, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', e=e), 404


if __name__ == "__main__":
    app.run(debug=True)
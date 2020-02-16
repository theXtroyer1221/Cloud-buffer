from flask import Flask, render_template, request
from forms import SignUpForm

import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cloud Buffer"
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    form = SignUpForm()

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
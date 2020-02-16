from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "ExpertMatbutik"
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
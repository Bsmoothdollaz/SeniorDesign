from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def view_home():
    return render_template("index.html", title="Home page")


@app.route("/404")
def view_404():
    return render_template("404.html", title="404")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/control")
def view_control():
    return render_template("control.html", title="Control")


@app.route("/flight")
def view_flight():
    return render_template("flight.html", title="Flight")


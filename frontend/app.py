from flask import Flask, request, render_template

app = Flask(__name__,static_url_path='/static') #Flask checks static folder for image files


@app.route("/")
def view_home():
    return render_template("index.html", title="Home page")


@app.route("/404")
def view_404():
    return render_template("404.html", title="404")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/control", methods = ["GET","POST"])
def view_control():
    if request.method == "POST":
        flightPlan = request.form.get
    return render_template("control.html", title="Control")


@app.route("/flight")
def view_flight():
    return render_template("flight.html", title="Flight")

@app.route("/help")
def view_help():
    return render_template("help.html", title="Help")

@app.route("/contact")
def view_contact():
    return render_template("contact.html", title="Contact")

if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
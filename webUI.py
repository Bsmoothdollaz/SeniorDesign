# Web UI to allow for Configuration, Control and Visualization of Drone delivery Project

from flask import Flask, render_template

app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/') #
# ‘/’ URL is bound with hello_world() function.
def homePage(): # Main page that user is directed to in order to begin flight
    return '<h1>' \
           '<center>DRONE DELIVERY PROJECT' \
           '</center></h1>' \
           '<h2><center> Choose Delivery Mode</center> </h2>' \
           '<button align="left">MANUAL</button>' \
           '<button align="right">AUTOMATIC</button>'

@app.route('/manual') # This page will lead to the manual mode
def manualMode():
    return 'This is manual mode'

@app.route('/automatic') # This page will lead to the manual mode
def automaticMode():
    return 'This is automatic mode'

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


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
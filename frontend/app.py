from flask import Flask, request, render_template
import sys
import time
import cv2
import logging
import constants as telloConstants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading
import tkinter as tk
from tkinter import *
from threading import *


app = Flask(__name__,static_url_path='/static') #Flask checks static folder for image files

telloDrone = Tello()
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

#Allows the drone connect
@app.route("/connect",methods=["POST"])
def connect():
    try:
        telloDrone.connect()
    except Exception as e:
        telloDrone.LOGGER.error(telloConstants.MESSAGES.failed_connect_drone)
        sys.exit('*** Exiting program. Could not connect to the drone.***')

# Allows the drone takeoff
@app.route("/takeoff", methods = ["POST"])
def takeoff():
    thread1 = Thread(target=telloDrone.takeoff)
    thread1.start()
    return ""

# Allows the drone land
@app.route("/land", methods = ["POST"])
def land():
    thread2 = Thread(target=telloDrone.land)
    thread2.start()
    return ""

# Allows the drone move right
@app.route("/right", methods = ["POST"])
def right():
    thread3 = Thread(target=telloDrone.move_right(50))
    thread3.start()
    return ""

# Allows the drone move left
@app.route("/left", methods = ["POST"])
def left():
    thread4 = Thread(target=telloDrone.move_left(50))
    thread4.start()
    return ""

# Allows the drone move up
@app.route("/up", methods = ["POST"])
def up():
    thread5 = Thread(target=telloDrone.move_up(50))
    thread5.start()
    return ""

# Allows the drone move down
@app.route("/down", methods = ["POST"])
def down():
    thread6 = Thread(target=telloDrone.move_down(50))
    thread6.start()
    return ""

# Allows the drone move forward
@app.route("/forward", methods = ["POST"])
def forward():
    thread7 = Thread(target=telloDrone.move_forward(50))
    thread7.start()
    return ""

# Allows the drone move backward
@app.route("/backward", methods = ["POST"])
def backward():
    thread8 = Thread(target=telloDrone.move_back(50))
    thread8.start()
    return ""


# Kill switch to end flight in case of abnormal behaviour
@app.route("/kill", methods = ["POST"])
def kill():
    thread9 = Thread(target=telloDrone.emergency)
    thread9.start()
    return ""


# Allows the drone rotate clockwise
@app.route("/rotatecw", methods = ["POST"])
def rotateCW():
    thread10 = Thread(target=telloDrone.rotate_clockwise(50))
    thread10.start()
    return ""

# Allows the drone rotate counterclockwise
@app.route("/rotateccw", methods = ["POST"])
def rotateCCW():
    thread11 = Thread(target=telloDrone.rotate_counter_clockwise(50))
    thread11.start()
    return ""
# Allows the drone pick the package
@app.route("/pick", methods = ["POST"])
def pick():
    # Do Something
    return ""

# Allows the drone drop the package
@app.route("/drop", methods = ["POST"])
def drop():
    # Do something
    return ""

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
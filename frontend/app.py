from flask import Flask, request, render_template, Response
import sys
import time
import cv2
import logging
import constants as telloConstants
import threading
# import tkinter as tk
# from tkinter import *
from threading import *

sys.path.append('../')
from DJITelloPy.api import Tello
from CameraController import CameraController

# Need to come back to the console and rerun the scripts

app = Flask(__name__, static_url_path='/static')  # Flask checks static folder for image files

global telloDrone
telloDrone = Tello()


@app.route("/")
def view_home():
    return render_template("index.html", title="Home page")

@app.route("/product")
def view_temp():
    return render_template("product.html", title="temp dev page")


@app.route("/404")
def view_404():
    return render_template("404.html", title="404")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/getFlightPlan", methods=["POST"])
def get_fplan():
    fplan = request.form['fplanfield']
    # print("FLIGHT PLAN: \n")
    print(fplan)
    return ""


@app.route("/control", methods=["GET", "POST"])
def view_control():
    drone_status = None
    try:
        drone_status = telloDrone.get_speed_x()
    except Exception as e:
        print('drone is not currently connected')
        return render_template("control.html", title="Control", speed=0)

    return render_template("control.html", title="Control", speed=telloDrone.get_speed_x())


@app.route("/flight", methods=['GET'])
def view_flight():
    return render_template("flight.html", title="Flight")


# Allows the drone connect
@app.route("/connect", methods=["POST"])
def connect():
    try:
        telloDrone.connect()
        isConnected = "Connected Successfully! You may begin flight"
        print(isConnected)
    except Exception as e:
        telloDrone.LOGGER.error(telloConstants.MESSAGES.failed_connect_drone)
        isConnected = "Failed to Connect, Please Try again"
        print(isConnected)
    return render_template("control.html", status=isConnected)


# Allows the drone takeoff
@app.route("/takeoff", methods=["POST"])
def takeoff():
    thread1 = Thread(target=telloDrone.takeoff)
    thread1.start()
    return ""


# Allows the drone land
@app.route("/land", methods=["POST"])
def land():
    thread2 = Thread(target=telloDrone.land)
    thread2.start()
    return ""


# Allows the drone move right
@app.route("/right", methods=["POST"])
def right():
    thread3 = Thread(target=telloDrone.move_right(50))
    thread3.start()
    return ""


# Allows the drone move left
@app.route("/left", methods=["POST"])
def left():
    thread4 = Thread(target=telloDrone.move_left(50))
    thread4.start()
    return ""


# Allows the drone move up
@app.route("/up", methods=["POST"])
def up():
    thread5 = Thread(target=telloDrone.move_up(50))
    thread5.start()
    return ""


# Allows the drone move down
@app.route("/down", methods=["POST"])
def down():
    thread6 = Thread(target=telloDrone.move_down(50))
    thread6.start()
    return ""


# Allows the drone move forward
@app.route("/forward", methods=["POST"])
def forward():
    thread7 = Thread(target=telloDrone.move_forward(50))
    thread7.start()
    return ""


# Allows the drone move backward
@app.route("/backward", methods=["POST"])
def backward():
    thread8 = Thread(target=telloDrone.move_back(50))
    thread8.start()
    return ""


# Kill switch to end flight in case of abnormal behaviour
@app.route("/kill", methods=["POST"])
def kill():
    thread9 = Thread(target=telloDrone.emergency)
    thread9.start()
    return ""


# Allows the drone rotate clockwise
@app.route("/rotatecw", methods=["POST"])
def rotateCW():
    thread10 = Thread(target=telloDrone.rotate_clockwise(50))
    thread10.start()
    return ""


# Allows the drone rotate counterclockwise
@app.route("/rotateccw", methods=["POST"])
def rotateCCW():
    thread11 = Thread(target=telloDrone.rotate_counter_clockwise(50))
    thread11.start()
    return ""


@app.route("/increase")
def incrSpeed():
    thread12 = Thread(target=telloDrone.set_speed(telloDrone.get_total_speed + 10))
    thread12.start()
    return render_template("control.html", speed=telloDrone.get_total_speed)


@app.route("/decrease")
def decrSpeed():
    thread13 = Thread(target=telloDrone.set_speed(telloDrone.get_total_speed - 10))
    thread13.start()
    return render_template("control.html", speed=telloDrone.get_total_speed)


# Allows the drone pick the package
@app.route("/pick", methods=["POST"])
def pick():
    # Do Something
    return ""


# Allows the drone drop the package
@app.route("/drop", methods=["POST"])
def drop():
    # Do something
    return ""


@app.route("/help")
def view_help():
    return render_template("help.html", title="Help")


@app.route("/contact")
def view_contact():
    return render_template("contact.html", title="Contact")


# Returns the battery level as a percentage
def get_battery_level():
    try:
        # Send the "battery?" command to the Tello drone
        response = telloDrone.get_battery()
        # Convert the response to an integer and return it as a percentage
        return int(response.text.strip()) / 100.0
    except Exception as e:
        # If there was an error, return -1
        print(f'Error getting battery level: {e}')
        return -1


@app.route("/get_battery", methods=['POST'])
def get_battery():
    battery_level = get_battery_level()

    # Render the HTML template with the battery level as a variable
    return render_template('navbar.html', battery_level=battery_level)


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return 5


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)

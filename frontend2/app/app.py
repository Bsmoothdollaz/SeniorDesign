from flask import Flask, request, render_template, Response
import sys

# import DJITelloPy.api.tello as Tello
import helpers
import time
# import cv2
import logging
# import constants as telloConstants
import threading
# import tkinter as tk
# from tkinter import *
from threading import *

sys.path.append('../../')
# from DJITelloPy.api import tello
# from CameraController import CameraController
import test_drone_connection

app = Flask(__name__, static_url_path='/static')  # Flask checks static folder for image files

# drone_thread = threading.Thread(target=helpers.get_connection_status, args=(), daemon=True, name='drone_connection')
# drone_thread.start()

global drone_wrapper
drone_wrapper = test_drone_connection.Custom_Drone()
drone_wrapper.try_connect()


@app.route("/")
def view_home():
    return render_template("index.html", title="Home")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/flight")
def view_flight():
    return render_template("flight.html", title="Flight")


@app.route("/support")
def view_support():
    return render_template("support.html", title="Support")


@app.route("/control")
def view_control():
    return render_template("control.html", title="Control")


@app.route("/validate_flight_plan", methods=["POST"])
def validate_flight_plan():
    f_plan = request.form['fplanfield']
    # At this point we have f_plan as a python variable that we can parse
    # and return a value if it is valid or not. Or explain what is not valid.
    response = helpers.backend_validate_flight_plan(f_plan)
    return 'done'


@app.route("/submit_flight_plan", methods=["POST"])
def submit_flight_plan():
    f_plan = request.form['fplanfield']
    response = helpers.backend_submit_flight_plan(f_plan)
    return 'done'


@app.route("/get_tello_battery", methods=["POST"])
def get_tello_battery():
    global drone_wrapper
    return str(drone_wrapper.get_battery())


@app.route("/get_connection_status", methods=["POST"])
def get_connection_status():
    response = helpers.get_tello_status()
    return response


@app.route("/takeoff", methods=["POST"])
def tello_takeoff():
    global drone_wrapper
    takeoff_thread = Thread(target=drone_wrapper.takeoff, args=())
    takeoff_thread.start()
    return "True"


@app.route("/land", methods=["POST"])
def tello_land():
    global drone_wrapper
    land_thread = Thread(target=drone_wrapper.land, args=())
    land_thread.start()
    # drone_wrapper.land()
    return "True"


@app.route("/connect_to_drone", methods=["POST"])
def connect_to_drone():
    global drone_wrapper
    drone_wrapper.try_connect()
    return "True"


@app.route("/emergency_shutoff", methods=["POST"])
def emergency_kill_drone():
    global drone_wrapper
    emergency_thread = Thread(target=drone_wrapper.emergency, args=())
    emergency_thread.start()


@app.route("/motor_on", methods=["POST"])
def turn_motor_on():
    global drone_wrapper
    motor_on_thread = Thread(target=drone_wrapper.motor_on, args=())
    motor_on_thread.start()


@app.route("/motor_off", methods=["POST"])
def turn_motor_off():
    global drone_wrapper
    motor_off_thread = Thread(target=drone_wrapper.motor_off, args=())
    motor_off_thread.start()


@app.route("/flip_forward", methods=["POST"])
def flip_forward():
    global drone_wrapper
    flip_forward_thread = Thread(target=drone_wrapper.flip, args=('f',))
    flip_forward_thread.start()


@app.route("/flip_backwards", methods=["POST"])
def flip_back():
    global drone_wrapper
    flip_back_thread = Thread(target=drone_wrapper.flip, args=('b',))
    flip_back_thread.start()


@app.route("/flip_left", methods=["POST"])
def flip_left():
    global drone_wrapper
    flip_left_thread = Thread(target=drone_wrapper.flip_forward, args=('l',))
    flip_left_thread.start()


@app.route("/flip_right", methods=["POST"])
def flip_right():
    global drone_wrapper
    flip_right_thread = Thread(target=drone_wrapper.flip_forward, args=('r',))
    flip_right_thread.start()


@app.route("/set_speed", methods=["POST"])
def set_drone_speed():
    global drone_wrapper
    speed = int(request.form["speed"])
    if speed < 10 or speed > 100:
        print('cant set speed to that amount')
        return 'Bad speed amount'
    set_speed_thread = Thread(target=drone_wrapper.set_speed, args=(speed,))
    set_speed_thread.start()


@app.route("/drone_move_udlr", methods=["POST"])
def drone_move_udlr():
    global drone_wrapper
    direction = str(request.form["direction"])
    distance = int(request.form["distance"])
    directions = ['up', 'down', 'left', 'right', 'forward', 'back']
    if direction not in directions:
        print('bad direction value')
        return 'Bad direction value'
    if distance < 20 or distance > 500:
        print('cant set distance to that amount')
        return 'Bad distance value'
    drone_udlr_thread = Thread(target=drone_wrapper.go_up_down_left_right, args=(direction,distance,))
    drone_udlr_thread.start()
    return 'here'


@app.route("/drone_rotate", methods=["POST"])
def rotate_drone():
    global drone_wrapper
    direction = str(request.form["direction"])
    degrees = int(request.form["degrees"])
    directions = ['cw', 'ccw']
    if direction not in directions:
        print('bad direction value')
        return 'bad direction value'
    if degrees < 1 or degrees > 360:
        print('cant rotate  to that amount')
        return 'bad degrees value'
    drone_rotate_thread = Thread(target=drone_wrapper.rotate_drone, args=(direction,degrees))
    drone_rotate_thread.start()
    return 'here'


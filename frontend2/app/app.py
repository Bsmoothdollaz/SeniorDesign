import flask
import numpy as np
from flask import Flask, request, render_template, Response
import sys
import socket
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
import json
import requests


sys.path.append('../../')
# from DJITelloPy.api import tello
# from CameraController import CameraController
import test_drone_connection
import parse_esp32_data


app = Flask(__name__, static_url_path='/static')  # Flask checks static folder for image files

# drone_thread = threading.Thread(target=helpers.get_connection_status, args=(), daemon=True, name='drone_connection')
# drone_thread.start()

global drone_wrapper
drone_wrapper = test_drone_connection.Custom_Drone()
drone_wrapper.try_connect()

ESP_TAG_HOST = ''  # Listen on all available interfaces
ESP_TAG_PORT = 8888  # Choose a port number
latest_data = ""  # Global variable to store the latest data received by the UDP socket


def udp_handler():
    global latest_data
    # Create a UDP socket and bind it to the specified host and port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ESP_TAG_HOST, ESP_TAG_PORT))
        print(f"Listening on {ESP_TAG_HOST}:{ESP_TAG_PORT}...")
        # Loop indefinitely, receiving and storing the latest data from the socket
        while True:
            data, addr = sock.recvfrom(1024)
            latest_data = data.decode('utf-8')
            # print(f"Received: {latest_data} from {addr}")


udp_thread = threading.Thread(target=udp_handler)
udp_thread.start()


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
    return ""


@app.route("/motor_off", methods=["POST"])
def turn_motor_off():
    global drone_wrapper
    motor_off_thread = Thread(target=drone_wrapper.motor_off, args=())
    motor_off_thread.start()
    return ""


@app.route("/flip", methods=["POST"])
def flip():
    directions = ['l', 'r', 'f', 'b']
    direction = str(request.form["button"])
    print(direction)
    if direction not in directions:
        print('bad direction')
        return ('bad direction')
    global drone_wrapper
    flip_forward_thread = Thread(target=drone_wrapper.flip, args=(direction,))
    flip_forward_thread.start()
    return render_template("control.html", direction=direction)


@app.route("/set_speed", methods=["GET", "POST"])
def set_drone_speed():
    global drone_wrapper
    print('raw speed:', request.form["speedSlider"])
    speed = int(request.form["speedSlider"])
    if speed < 10 or speed > 100:
        print('cant set speed to that amount')
        return 'Bad speed amount'
    set_speed_thread = Thread(target=drone_wrapper.set_speed, args=(speed,))
    set_speed_thread.start()
    return render_template("control.html", speed=speed)


@app.route("/drone_move", methods=["POST"])
def drone_move():
    global drone_wrapper
    direction = str(request.form["button"])
    distance = int(request.form["value"])
    directions = ['up', 'down', 'left', 'right', 'forward', 'back']
    print("Direction: ", direction)
    print("Distance: ", distance)
    if direction not in directions:
        print('bad direction value')
        return 'Bad direction value'
    if distance < 20 or distance > 500:
        print('Cannot set distance to that amount')
        return 'Bad distance value'
    drone_udlr_thread = Thread(target=drone_wrapper.go_up_down_left_right, args=(direction, distance,))
    drone_udlr_thread.start()
    return render_template("control.html", direction=direction, distance=distance)


@app.route("/drone_rotate", methods=["POST"])
def rotate_drone():
    global drone_wrapper
    direction = str(request.form["button"])
    degrees = int(request.form["value"])
    directions = ['cw', 'ccw']
    print("Direction: ", direction)            # print(f"Received: {latest_data} from {addr}")

    print("Degrees: ", degrees)
    if direction not in directions:
        print('bad direction value')
        return 'bad direction value'
    if degrees < 1 or degrees > 360:
        print('cant rotate  to that amount')
        return 'bad degrees value'
    drone_rotate_thread = Thread(target=drone_wrapper.rotate_drone, args=(direction, degrees))
    drone_rotate_thread.start()
    return render_template("control.html", direction=direction, degrees=degrees)


@app.route("/get_tello_data", methods=["GET"])
def get_tello_data():
    global drone_wrapper
    if drone_wrapper is None:
        return 'No data'
    else:
        print('Data:', drone_wrapper.get_drone_state())
        return json.dumps(drone_wrapper.get_drone_state(), indent=4)


@app.route('/get_latest_esp32_data', methods=["GET"])
def get_latest_data():
    global latest_data
    return latest_data


@app.route("/get_drone_coords", methods=["GET"])
def get_drone_coords():
    global drone_wrapper
    if drone_wrapper is None:
        return 'No data'
    else:
        # set this value when the anchors are deployed
        # (-) value if B is to the right of A
        tag_positions = parse_esp32_data.get_tag_location(-2.0828)
        if tag_positions is None:
            return 'No tag positions'
        else:
            x, y = tag_positions
            return f'x={x}, y={y}'

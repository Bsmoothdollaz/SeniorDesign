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

drone_thread = threading.Thread(target=helpers.get_connection_status, args=(), daemon=True, name='drone_connection')
drone_thread.start()


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
    return str(test_drone_connection.get_battery())


@app.route("/get_connection_status", methods=["POST"])
def get_connection_status():
    response = helpers.get_tello_status()
    return response


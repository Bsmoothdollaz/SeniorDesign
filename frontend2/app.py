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

app = Flask(__name__, static_url_path='/static')  # Flask checks static folder for image files


@app.route("/")
def view_home():
    return render_template("index.html", title="Home")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/validate_flight_plan", methods=["POST"])
def validate_flight_plan():
    f_plan = request.form['fplanfield']
    # At this point we have f_plan as a python variable that we can parse
    # and return a value if it is valid or not. Or explain what is not valid.
    return 'done'


@app.route("/submit_flight_plan", methods=["POST"])
def submit_flight_plan():
    f_plan = request.form['fplanfield']
    # At this point we have f_plan as a python variable that we send somewhere else
    return 'done'

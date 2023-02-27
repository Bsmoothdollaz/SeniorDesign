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
    return render_template("index.html", title="Home page")

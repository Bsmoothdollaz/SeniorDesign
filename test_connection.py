import sys
import time
import DJITelloPy.api.tello
import constants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading

global drone
drone = Tello()


def run():
    while 1:
        print(drone.isDroneConnected())
        time.sleep(5)

import sys
import time
import DJITelloPy.api.tello
from DJITelloPy.api import Tello
# from CameraController import CameraController
import threading


class Custom_Drone:
    def __init__(self):
        self.drone = None

    def get_drone_object(self):
        return self.drone


def get_battery():
    drone = Tello()
    battery = None
    try:
        drone.connect()
        battery = drone.get_battery()
    except Exception as TelloException:
        battery = None
    return str(battery)

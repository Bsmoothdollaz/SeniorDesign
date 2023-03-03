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

    def try_connect(self):
        self.drone = Tello()
        try:
            self.drone.connect()
        except Exception as e:
            print('could not connect to drone')

    def get_battery(self):
        drone = self.get_drone_object()
        if drone is None:
            return str(None)
        else:
            try:
                battery = drone.get_battery()
            except Exception as TelloException:
                battery = None
        return str(battery)

    def takeoff(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("takeoff", timeout=Tello.TAKEOFF_TIMEOUT)
        except Exception as e:
            print('exception on takeoff', e)

    def land(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("land", timeout=Tello.TAKEOFF_TIMEOUT)
        except Exception as e:
            print('exception on land', e)


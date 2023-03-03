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
            self.drone = None

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

    def emergency(self):
        drone = self.get_drone_object()
        try:
            drone.send_command_without_return("emergency")
        except Exception as E:
            print('exception on emergency', e)

    def motor_on(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("motoron")
        except Exception as E:
            print('exception on motor on', e)

    def motor_off(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("motoroff")
        except Exception as E:
            print('exception on motor off', e)

    def flip(self, direction):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("flip {}".format(direction))
        except Exception as e:
            print('exception on flip', e)

    def set_speed(self, speed):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("speed {}".format(speed))
        except Exception as e:
            print('exception on set speed', e)

    def go_up_down_left_right(self, direction, distance):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("{} {}".format(direction, distance))
        except Exception as e:
            print('exception on up down left right', e)

    def rotate_drone(self, direction, degrees):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("{} {}".format(direction, degrees))
        except Exception as e:
            print('exception rotate drone', e)

import sys
import time
import DJITelloPy.api.tello
from DJITelloPy.api import Tello
# from CameraController import CameraController
import threading
# import cv2
import socket
# from PIL import Image, ImageTk
# import tkinter as tki
# from tkinter import Toplevel, Scale
import threading
import datetime
# import cv2
import os
import time
import platform


class Custom_Drone:
    def __init__(self):
        self.drone = None

    def get_drone_object(self):
        return self.drone

    def try_connect(self):
        self.drone = Tello()
        try:
            self.drone.connect()
            time.sleep(2)
            self.drone.send_control_command("streamon")
            self.drone.set_video_bitrate(Tello.BITRATE_5MBPS)
            self.drone.set_video_resolution('high')
            self.drone.enable_mission_pads()
        except Exception as e:
            print('could not connect to drone', e)
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
            print('exception on emergency', E)

    def motor_on(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("motoron")
        except Exception as E:
            print('exception on motor on', E)

    def motor_off(self):
        drone = self.get_drone_object()
        try:
            drone.send_control_command("motoroff")
        except Exception as E:
            print('exception on motor off', E)

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

    def get_drone_state(self):
        drone = self.get_drone_object()
        state = None
        try:
            state = drone.get_current_state()
        except Exception as e:
            print('exception while getting state data', e)
        return state

    def get_mission_pad(self):
        drone = self.get_drone_object()
        test_id = -1
        try:
            test_id = int(drone.get_mission_pad_id())
        except Exception as e:
            print('Caught exception in mission pad')
        return test_id

    def get_yaw_drone(self):
        drone = self.get_drone_object()
        yaw = None
        try:
            yaw = drone.get_yaw()
        except Exception as e:
            print('caught exception while getting the yaw ')
        return yaw

    def center_mission_pad(self, pad):
        drone = self.get_drone_object()
        try:
            drone.go_xyz_speed_mid(0,0,50,10,pad)
            time.sleep(2)
        except Exception as e:
            print('EXCEPTION WHILE CENTERING ON MISSION PAD')
        return


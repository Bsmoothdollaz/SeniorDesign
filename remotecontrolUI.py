import sys
import time
import cv2
import logging
import constants as telloConstants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading
import tkinter as tk
from tkinter import *
from threading import *
# from DJITelloPy.api import GUI
# buttonPressed = False










state_logging_interval = 0.5  # seconds
mission_pad_logging_interval = 0.5



def mission_pad_logger(telloDrone, mission_pad_logging_interval):
    time.sleep(mission_pad_logging_interval)
    if telloDrone.get_mission_pad_id() != 1:
        telloDrone.LOGGER.info('misison pad number detected:{}'.format(telloDrone.get_mission_pad_id()))

        move_x = telloDrone.get_mission_pad_distance_x()
        move_y = telloDrone.get_mission_pad_distance_y()
        move_z = telloDrone.get_mission_pad_distance_z()

    mission_pad_logger(telloDrone, mission_pad_logging_interval)


def log_before_execution(telloDrone):
    telloDrone.LOGGER.info('data goes here')
    telloDrone.LOGGER.info('ATTITUDE: {}'.format(telloDrone.query_attitude()))
    telloDrone.LOGGER.info('BAROMETER: {}'.format(telloDrone.query_barometer()))
    telloDrone.LOGGER.info('BATTERY: {}'.format(telloDrone.query_battery()))
    telloDrone.LOGGER.info('TOF_DISTANCE: {} '.format(telloDrone.query_distance_tof()))
    telloDrone.LOGGER.info('WIFI_SIGNAL_NOISE RATIO: {}'.format(telloDrone.query_wifi_signal_noise_ratio()))
    telloDrone.LOGGER.info('SDK VERSION: {}'.format(telloDrone.query_sdk_version()))
    telloDrone.LOGGER.info('SERIAL NUMBER: {}'.format(telloDrone.query_serial_number()))


def log_state(interval_sec, telloDrone):
    time.sleep(interval_sec)
    telloDrone.LOGGER.info('PERIODIC STATE VALUES: {}'.format(telloDrone.get_current_state()))
    log_state(interval_sec, telloDrone)





""" CONNECT TO THE DRONE"""
telloDrone = Tello()
telloDrone.LOGGER.info(telloConstants.MESSAGES.try_connect_drone)
# telloUI = GUI(telloDrone)
# telloUI.window.mainloop()

try:
    telloDrone.connect()
except Exception as e:
    telloDrone.LOGGER.error(telloConstants.MESSAGES.failed_connect_drone)
    sys.exit('*** Exiting program. Could not connect to the drone.***')

def goUp():
    telloDrone.move_up(50)
    time.sleep(1)

def threadUp():
    t1 = Thread(target=goUp)
    t1.start()
def goDown():
    telloDrone.move_down(50)
    time.sleep(1)
def threadDown():
    t2 = Thread(target=goDown)
    t2.start()

def goLeft():
    telloDrone.move_left(50)
    time.sleep(1)
def threadLeft():
    t3 = Thread(target=goLeft)
    t3.start()

def goRight():
    telloDrone.move_right(50)
    time.sleep(1)
def threadRight():
    t4 = Thread(target=goRight)
    t4.start()

def threadTakeoff():
    t5 = Thread(target=telloDrone.takeoff)
    t5.start()

def threadLand():
    t6 = Thread(target=telloDrone.land)
    t6.start()


def threadKill():
    t7 = Thread(target=telloDrone.emergency)
    t7.start()


def goForward():
    telloDrone.move_forward(50)
    time.sleep(1)
def threadForward():
    t8 = Thread(target=goForward)
    t8.start()

def goBackward():
    telloDrone.move_back(50)
    time.sleep(1)
def threadBackward():
    t9 = Thread(target=goBackward)
    t9.start()

def rotateC():
    telloDrone.rotate_clockwise(180)
    time.sleep(1)

def threadC():
    t10 = Thread(target=rotateC)
    t10.start()

def rotateCC():
    telloDrone.rotate_counter_clockwise(180)
    time.sleep(1)

def threadCC():
    t11 = Thread(target=rotateCC)
    t11.start()

telloUI = tk.Tk()
telloUI.geometry("400x300")
telloUI.title("CONTROLLER")
telloUI.configure(bg='beige')
# Keys: Up, Down, Left, Right, KillSwitch, Takeoff, Rotate (Clockwise and Counter-Clockwise), Land
upButton = tk.Button(telloUI, text="↑", command=threadUp)
upButton.place(x=165, y=50,width=80,height=40)

downButton = tk.Button(telloUI, text="↓", command=threadDown)
downButton.place(x=165, y=90,width=80,height=40)

leftButton = tk.Button(telloUI, text="←", command=threadLeft)
leftButton.place(x=85, y=70,width=80,height=40)

rightButton = tk.Button(telloUI, text="→", command=threadRight)
rightButton.place(x=245, y=70, width=80,height=40)

takeOffButton = tk.Button(telloUI, text="TAKEOFF", command=threadTakeoff)
takeOffButton.place(x=5, y=20,width=80,height=40)

landButton = tk.Button(telloUI, text="LAND", command=threadLand)
landButton.place(x=315, y=20,width=80,height=40)

killButton = tk.Button(telloUI, text="KILL", command=threadKill)
killButton.place(x=315, y=140,width=80,height=40)

forwardButton = tk.Button(telloUI,text="FORWARD",command=threadForward)
forwardButton.place(x=5,y=140,width=80,height=40)

backwardButton = tk.Button(telloUI,text="BACKWARD",command=threadBackward)
backwardButton.place(x=85,y=140,width=80,height=40)

rotateCButton = tk.Button(telloUI,text="CLOCKWISE",command=threadC)
rotateCButton.place(x=65,y=200,width=140,height=40)

rotateCCButton = tk.Button(telloUI,text="COUNTER-CLOCKWISE",command=threadCC)
rotateCCButton.place(x=205,y=200,width=140,height=40)


telloUI.mainloop()



start_time = time.time()
telloDrone.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
exit(1)
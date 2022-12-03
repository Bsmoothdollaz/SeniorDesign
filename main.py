import sys
import time
import cv2
import logging
import constants as telloConstants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading
import tkinter
from tkinter import *
from DJITelloPy.api import GUI
buttonPressed = False










state_logging_interval = 0.5  # seconds
mission_pad_logging_interval = 0.5



def mission_pad_logger(telloDrone, mission_pad_logging_interval):
    time.sleep(mission_pad_logging_interval)
    if telloDrone.get_mission_pad_id() != 1:
        telloDrone.LOGGER.info('misison pad number detected:{}'.format(tello.get_mission_pad_id()))

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

try:
    telloDrone.connect()
except Exception as e:
    telloDrone.LOGGER.error(telloConstants.MESSAGES.failed_connect_drone)
    sys.exit('*** Exiting program. Could not connect to the drone.***')

telloDrone.LOGGER.info(telloConstants.MESSAGES.successful_connect_drone)

# Function to move up


# Start the periodic drone state logger
state_logger = threading.Thread(target=log_state, args=(state_logging_interval, telloDrone), daemon=True, name='state-logger')
state_logger.start()

# tello.set_video_bitrate(Tello.BITRATE_1MBPS)
# tello.set_video_resolution(Tello.RESOLUTION_720P)
camera = CameraController(tello=tello)
# camera.run_bottom_cam()
camera.run_front_cam()
""" DO SOME PRE-FLIGHT ACTIONS """
telloDrone.enable_mission_pads()
telloDrone.set_mission_pad_detection_direction(0)
start_time = time.time()  # start the flight timer
telloDrone.turn_motor_on()
try:
    log_before_execution(telloDrone)
except Exception as e:
    pass



""" EXECUTE THE DRONE FLIGHT """
time.sleep(5)
tello.takeoff()


# time.sleep(5)

""" USER INPUT TO MOVE DRONE IN DIFFERENT DIRECTIONS"""




""" READY TO LAND THE DRONE"""
tello.land()
tello.turn_motor_on()
time.sleep(5)
tello.turn_motor_off()




""" Gracefully close any resources """
# daemon threads are joined by default
# log_before_execution(tello)
tello.streamoff()
tello.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
exit(1)




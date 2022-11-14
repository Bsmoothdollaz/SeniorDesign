import sys
import time
import cv2
import logging
import constants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading

state_logging_interval = 0.5  # seconds


def log_before_execution(tello):
    tello.LOGGER.info('data goes here')
    tello.LOGGER.info('ATTITUDE: {}'.format(tello.query_attitude()))
    tello.LOGGER.info('BAROMETER: {}'.format(tello.query_barometer()))
    tello.LOGGER.info('BATTERY: {}'.format(tello.query_battery()))
    tello.LOGGER.info('TOF_DISTANCE: {} '.format(tello.query_distance_tof()))
    tello.LOGGER.info('WIFI_SIGNAL_NOISE RATIO: {}'.format(tello.query_wifi_signal_noise_ratio()))
    tello.LOGGER.info('SDK VERSION: {}'.format(tello.query_sdk_version()))
    tello.LOGGER.info('SERIAL NUMBER: {}'.format(tello.query_serial_number()))


def log_state(interval_sec, tello):
    time.sleep(interval_sec)
    tello.LOGGER.info('PERIODIC STATE VALUES: {}'.format(tello.get_current_state()))
    log_state(interval_sec, tello)


""" CONNECT TO THE DRONE"""
tello = Tello()
tello.LOGGER.info(constants.MESSAGES.try_connect_drone)

try:
    tello.connect()
except Exception as e:
    tello.LOGGER.error(constants.MESSAGES.failed_connect_drone)
    sys.exit('*** Exiting program. Could not connect to the drone.***')

tello.LOGGER.info(constants.MESSAGES.successful_connect_drone)

# Start the periodic drone state logger
state_logger = threading.Thread(target=log_state, args=(state_logging_interval, tello), daemon=True, name='state-logger')
state_logger.start()

camera = CameraController(tello=tello)
camera.run_front_cam()
# camera.run_bottom_cam()
start_time = time.time()  # start the flight timer

""" DO SOME PRE-FLIGHT ACTIONS """
tello.turn_motor_on()
try:
    log_before_execution(tello)
except Exception as e:
    pass
time.sleep(10)
print('taking off')

""" EXECUTE THE DRONE FLIGHT """
tello.takeoff()
time.sleep(10)

""" READY TO LAND THE DRONE"""
tello.land()
tello.turn_motor_on()
time.sleep(5)
tello.turn_motor_off()

""" Gracefully close any resources """
# daemon threads are joined by default
log_before_execution(tello)

tello.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
exit(1)

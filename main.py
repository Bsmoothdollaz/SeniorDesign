import sys
import time
import cv2
import logging
import constants
from DJITelloPy.api import Tello
import threading

global frame_read
state_logging_interval = 0.5
keepRecording = True


def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    global frame_read
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


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


def main():
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
    daemon = threading.Thread(target=log_state, args=(state_logging_interval, tello), daemon=True, name='state-logger')
    daemon.start()

    recorder = threading.Thread(target=videoRecorder)
    recorder.start()

    start_time = time.time()  # start the flight timer

    tello.streamon()
    global frame_read
    frame_read = tello.get_frame_read()

    """ DO SOME PRE-FLIGHT ACTIONS """
    tello.turn_motor_on()
    time.sleep(5)
    log_before_execution(tello)

    """ EXECUTE THE DRONE FLIGHT """
    # tello.takeoff()
    # time.sleep(10)

    """ READY TO LAND THE DRONE"""
    # tello.land()
    # tello.turn_motor_on()
    # time.sleep(5)
    tello.turn_motor_off()

    """ Gracefully close any resources """
    log_before_execution(tello)
    tello.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
    exit(1)


if __name__ == '__main__':
    main()

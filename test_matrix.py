import sys
import time
import cv2
import logging

import DJITelloPy.api.tello
import constants
from DJITelloPy.api import Tello
from CameraController import CameraController
import threading

state_logging_interval = 0.5  # seconds


def log_before_execution(tello):
    try:
        tello.LOGGER.info('data goes here')
        tello.LOGGER.info('BATTERY: {}'.format(tello.get_battery()))
        if tello.get_battery() < 30:
            tello.LOGGER.error('*** REPLACE BATTERY ***')
            tello.turn_motor_off()
            exit(2)
        tello.LOGGER.info('ATTITUDE: {}'.format(tello.query_attitude()))
        tello.LOGGER.info('BAROMETER: {}'.format(tello.query_barometer()))
        tello.LOGGER.info('TOF_DISTANCE: {} '.format(tello.query_distance_tof()))
        tello.LOGGER.info('WIFI_SIGNAL_NOISE RATIO: {}'.format(tello.query_wifi_signal_noise_ratio()))
        tello.LOGGER.info('SDK VERSION: {}'.format(tello.query_sdk_version()))
        tello.LOGGER.info('SERIAL NUMBER: {}'.format(tello.query_serial_number()))
    except ValueError as ve:
        print('caught value error')


def log_state(interval_sec, tello):
    time.sleep(interval_sec)
    tello.LOGGER.info('PERIODIC STATE VALUES: {}'.format(tello.get_current_state()))
    log_state(interval_sec, tello)


""" CONNECT TO THE DRONE"""
tello = Tello()
tello.LOGGER.info(constants.MESSAGES.try_connect_drone)

try:
    try:
        tello.connect()
    except Exception as e:
        tello.LOGGER.error(constants.MESSAGES.failed_connect_drone)
        sys.exit('*** Exiting program. Could not connect to the drone.***')

    tello.LOGGER.info(constants.MESSAGES.successful_connect_drone)
    tello.send_control_command('EXT mled g 00000000')            # clear the display
    tello.send_control_command('EXT led 0 0 0')           # clear to top led
    try:
        log_before_execution(tello)
    except Exception as e:
        print('caught a log exception',e)
        exit(1)
    time.sleep(2)

    # Start the camera thread
    tello.set_video_bitrate(Tello.BITRATE_5MBPS)
    tello.set_video_resolution(Tello.RESOLUTION_480P)
    camera = CameraController(tello=tello)
    # camera.run_front_cam()
    camera.run_bottom_cam()

    # Start the periodic drone state logger
    state_logger = threading.Thread(target=log_state, args=(state_logging_interval, tello), daemon=True, name='state-logger')
    state_logger.start()

    start_time = time.time()  # start the flight timer

    """ DO SOME PRE-FLIGHT ACTIONS """
    try:
        tello.turn_motor_on()
    except Exception as e:
        tello.turn_motor_off()
        tello.turn_motor_on()

    """ COUNT DOWN ON THE MATRIX BEFORE TAKING OFF """
    for i in range(5,0,-1):
        try:
            tello.send_control_command('EXT mled s b {}'.format(i))
        except DJITelloPy.api.tello.TelloException as e:
            print('caught an excepton!')
        time.sleep(1)
    tello.send_control_command('EXT mled g 00000000')            # clear display

    """ DRONE TAKE OFF AND PREFORM FLIGHT"""
    tello.send_control_command('EXT led br 1 0 0 255')    # breathing effect with frequency and color
    time.sleep(2)   # cool down the udp port before takeoff
    tello.takeoff()
    #
    # tello.move_right(20)
    #
    # curr_pad = -1
    # while tello.get_mission_pad_id() != -1:
    #     tello.send_control_command('EXT mled s b {}'.format(tello.get_mission_pad_id()))
    #     curr_pad = tello.get_mission_pad_id()
    #     break
    # time.sleep(2)
    # starting_height = tello.get_height()
    # print('starting height', starting_height)
    # tello.go_xyz_speed_mid(0,0,starting_height,20,curr_pad)
    # for i in range(3):
    #     tello.move_down(20)
    #     time.sleep(0.5)
    #     print('height:', tello.get_height())



    # tello.move_forward(210)
    # while tello.get_mission_pad_id() != -1:
    #     # tello.send_control_command('EXT mled s b {}'.format(tello.get_mission_pad_id()))
    #     # time.sleep(2)
    #     tello.go_xyz_speed_mid(0,0,30,50,7)
    #     tello.rotate_clockwise(360)
    #     tello.go_xyz_speed_mid(0,0,30,50,7)
    #     break


    tello.land()



    # tello.send_control_command('EXT led 0 0 255')           # set the top led to a static color
    # tello.send_control_command('EXT led bl 1 0 0 255 255 255 0')    # blink between two colors at frequency
    # tello.send_control_command('EXT mled g rrrbb0pp')            # set colors for matrix
    # tello.send_control_command('EXT mled l b 2.5 1')     # display a string

    # tello.send_control_command('EXT mled s b 1')    # display a static ascii character

    # tello.send_control_command('EXT mled sg 0000')  #

except KeyboardInterrupt as e:
    tello.emergency()




""" Gracefully close any resources """
# daemon threads are joined by default
log_before_execution(tello)
tello.send_control_command('EXT mled g 00000000')            # clear the display
tello.send_control_command('EXT led 0 0 0')           # clear to top led
tello.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
exit(1)

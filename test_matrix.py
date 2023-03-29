import sys
import time
import DJITelloPy.api.tello
from DJITelloPy.api import Tello
# from CameraController import CameraController
import threading

state_logging_interval = 0.5  # seconds


def log_before_execution(tello):
    try:
        tello.LOGGER.info('data goes here')
        tello.LOGGER.info('BATTERY: {}'.format(tello.get_battery()))
        if tello.get_battery() < 60:
            tello.LOGGER.error('*** BATTERY < 60 FLIPS MIGHT NOT WORK ***')
        elif tello.get_battery() < 30:
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
        print('caught value error', ve)


def log_state(interval_sec, tello):
    time.sleep(interval_sec)
    tello.LOGGER.info('PERIODIC STATE VALUES: {}'.format(tello.get_current_state()))
    log_state(interval_sec, tello)


def find_mission_pad(tello):
    while tello.get_mission_pad_id() != -1:
        try:
            detected_pad = tello.get_mission_pad_id()
            tello.send_control_command('EXT mled s p {}'.format(detected_pad))
            tello.go_xyz_speed_mid(0, 0, 50, 20, detected_pad)
            tello.move_up(30)
            tello.rotate_clockwise(360)
            tello.go_xyz_speed_mid(0, 0, 50, 20, detected_pad)
            return
        except Exception as e:
            print('caught an exception when detecting a mission pad', e)
            tello.LOGGER.error('EXCEPTION WHILE DETECTING MISSION PAD', e)


""" CONNECT TO THE DRONE"""
tello = Tello()
# tello.LOGGER.info(constants.MESSAGES.try_connect_drone)

try:
    try:
        tello.connect()
    except Exception as e:
        # tello.LOGGER.error(constants.MESSAGES.failed_connect_drone)
        sys.exit('*** Exiting program. Could not connect to the drone.***')

    # tello.LOGGER.info(constants.MESSAGES.successful_connect_drone)
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
    tello.set_video_resolution('high')
    # camera = CameraController(tello=tello)
    # # camera.run_front_cam()
    # camera.run_bottom_cam()

    # Start the periodic drone state logger
    state_logger = threading.Thread(target=log_state, args=(state_logging_interval, tello), daemon=True, name='state-logger')
    state_logger.start()

    start_time = time.time()  # start the flight timer

    """ DO SOME PRE-FLIGHT ACTIONS / COOL OFF THE BATTERY BEFORE FLIGHT """
    try:
        tello.turn_motor_on()
    except Exception as e:
        tello.turn_motor_off()
        tello.turn_motor_on()

    """ COUNT DOWN ON THE MATRIX BEFORE TAKING OFF """
    for i in range(5,0,-1):
        try:
            tello.send_control_command('EXT mled s p {}'.format(i))
        except DJITelloPy.api.tello.TelloException as e:
            print('caught an excepton!')
        time.sleep(1)
    tello.send_control_command('EXT mled g 00000000')            # clear display

    """ DRONE TAKE OFF AND PREFORM FLIGHT"""
    tello.send_control_command('EXT led br 1 0 0 255')    # breathing effect with frequency and color
    time.sleep(1)   # cool down the udp port before takeoff
    tello.takeoff()

    tello.send_control_command('EXT mled sl 255')   # full brightness on the matrix
    # first mission pad
    try:
        find_mission_pad(tello)
    except Exception as e:
        tello.send_control_command('EXT led br 1 255 0 0')
        time.sleep(3)
        tello.land()
        exit('NO MISSION PAD 1 FOUND')

    time.sleep(1)
    tello.move_up(30)           # help our mission pad detection range by moving up
    tello.move_forward(215)

    # second mission pad
    try:
        find_mission_pad(tello)
    except Exception as e:
        tello.send_control_command('EXT led br 1 255 0 0')
        time.sleep(3)
        tello.land()
        exit('NO MISSION PAD 2 FOUND')
    time.sleep(1)
    tello.rotate_counter_clockwise(90)
    tello.move_up(30)  # help our mission pad detection range by moving up
    tello.move_forward(145)    # 160

    # third mission pad
    try:
        find_mission_pad(tello)
    except Exception as e:
        tello.send_control_command('EXT led br 1 255 0 0')
        time.sleep(3)
        tello.land()
        exit('NO MISSION PAD 3 FOUND')
    time.sleep(2)

    # flips coming, change the status color to indicate a warning
    tello.send_control_command('EXT led br 1.5 255 0 0')  # breathing effect with frequency and color RED
    try:
        tello.move_up(100)
        tello.flip_back()
    except Exception as e:
        tello.LOGGER.warn('COULD NOT FLIP THE DRONE BACK!!! CONTINUING')
        pass

    try:
        tello.flip_left()
    except Exception as e:
        tello.LOGGER.warn('COULD NOT FLIP THE DRONE LEFT!!! CONTINUING')
        pass

    smily_face = '0p0000p0' \
                 '0p0000p0' \
                 '00000000' \
                 '00000000' \
                 '00000000' \
                 '0p0000p0' \
                 '0pppppp0'

    tello.send_control_command('EXT led 255 255 0')
    tello.send_control_command('EXT mled g {}'.format(smily_face))

    tello.rotate_clockwise(360)
    time.sleep(2)
    tello.rotate_counter_clockwise(360)

    # locate the final mission pad
    find_mission_pad(tello)

    tello.land()

except KeyboardInterrupt as e:
    tello.emergency()

""" Gracefully close any resources """
# daemon threads are joined by default
log_before_execution(tello)
tello.send_control_command('EXT mled g 00000000')            # clear the display
tello.send_control_command('EXT led 0 0 0')           # clear to top led
tello.LOGGER.info("EXECUTION TIME: --- %s seconds ---" % (time.time() - start_time))
exit(1)

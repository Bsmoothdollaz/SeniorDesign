import random

import flask
import matplotlib
import numpy as np
from flask import Flask, request, render_template, Response, jsonify
import sys
import socket
# import DJITelloPy.api.tello as Tello
import helpers
import time
import cv2
import logging
# import constants as telloConstants
import threading
# import tkinter as tk
# from tkinter import *
from threading import *
import json
import requests
from filterpy.kalman import KalmanFilter
from numpy import matrix, array
import matplotlib.pyplot as plt
import socket
import threading

sys.path.append('../../')
# from DJITelloPy.api import tello
# from CameraController import CameraController
import test_drone_connection
import parse_esp32_data

app = Flask(__name__, static_url_path='/static')  # Flask checks static folder for image files

# drone_thread = threading.Thread(target=helpers.get_connection_status, args=(), daemon=True, name='drone_connection')
# drone_thread.start()

global drone_wrapper
drone_wrapper = test_drone_connection.Custom_Drone()
drone_wrapper.try_connect()

ESP_TAG_HOST = ''  # Listen on all available interfaces
ESP_TAG_PORT = 8888  # Choose a port number
latest_data = ""  # Global variable to store the latest data received by the UDP socket

drop_locations = []
flight_plan = []


def udp_handler():
    global latest_data
    # Create a UDP socket and bind it to the specified host and port
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ESP_TAG_HOST, ESP_TAG_PORT))
        print(f"Listening on {ESP_TAG_HOST}:{ESP_TAG_PORT}...")
        # Loop indefinitely, receiving and storing the latest data from the socket
        while True:
            data, addr = sock.recvfrom(1024)
            latest_data = data.decode('utf-8')
            # print(f"Received: {latest_data} from {addr}")


udp_thread = threading.Thread(target=udp_handler)
udp_thread.start()


@app.route("/")
def view_home():
    return render_template("index.html", title="Home")


@app.route("/config")
def view_config():
    return render_template("config.html", title="Config")


@app.route("/flight")
def view_flight():
    return render_template("flight.html", title="Flight")


@app.route("/support")
def view_support():
    return render_template("support.html", title="Support")


@app.route("/control")
def view_control():
    return render_template("control.html", title="Control")


@app.route("/validate_flight_plan", methods=["POST"])
def validate_flight_plan():
    f_plan = request.form['fplanfield']
    # At this point we have f_plan as a python variable that we can parse
    # and return a value if it is valid or not. Or explain what is not valid.
    response = helpers.backend_validate_flight_plan(f_plan)
    return 'done'


@app.route("/submit_flight_plan", methods=["POST"])
def submit_flight_plan():
    global flight_plan
    f_plan = request.form['fplanfield']

    temp_f_plan = []
    # parse f_plan into a list of instructions
    instructions = f_plan.split(';')
    for i in instructions:
        temp_f_plan.append(i)

    flight_plan = temp_f_plan
    print('set global flight_plan', flight_plan)

    return 'done'


@app.route("/get_flight_plan", methods=['GET'])
def get_flight_plan():
    global flight_plan
    if len(flight_plan) == 0:
        data = {}
        return jsonify(data)

    data = []  # list of instruction dictionaries
    previous_dst = None

    counter = 0
    for instruction in flight_plan:
        if len(instruction) > 1:
            src, dst = instruction.split('->')
            src = src.strip()
            dst = dst.strip()

            if counter == 0:
                if src != "Home":
                    return jsonify({"error": f"Invalid flight plan. Instruction {counter} should start from 'Home'."})
            else:
                # Check if src of current instruction is the same as the previous dst
                if src != previous_dst:
                    return jsonify(
                        {
                            "error": f"Invalid flight plan. Instruction {counter}'s source does not match previous destination."})

            data.append({
                'instruction_number': counter,
                'dst': dst.strip(),
                'src': src.strip()

            })

            previous_dst = dst
            counter += 1

    return jsonify(data)


@app.route("/get_tello_battery", methods=["POST"])
def get_tello_battery():
    global drone_wrapper
    return str(drone_wrapper.get_battery())


@app.route("/get_connection_status", methods=["POST"])
def get_connection_status():
    response = helpers.get_tello_status()
    return response


@app.route("/takeoff", methods=["POST"])
def tello_takeoff():
    global drone_wrapper
    takeoff_thread = Thread(target=drone_wrapper.takeoff, args=())
    takeoff_thread.start()
    return "True"


@app.route("/land", methods=["POST"])
def tello_land():
    global drone_wrapper
    land_thread = Thread(target=drone_wrapper.land, args=())
    land_thread.start()
    # drone_wrapper.land()
    return "True"


@app.route("/connect_to_drone", methods=["POST"])
def connect_to_drone():
    global drone_wrapper
    drone_wrapper.try_connect()
    return "True"


@app.route("/emergency_shutoff", methods=["POST"])
def emergency_kill_drone():
    global drone_wrapper
    if drone_wrapper is None:
        return jsonify({"error": "Drone not initialized"}), 500

    emergency_thread = Thread(target=drone_wrapper.emergency, args=())
    emergency_thread.start()
    return jsonify({"success": "Emergency stop initiated"}), 200


@app.route("/motor_on", methods=["POST"])
def turn_motor_on():
    global drone_wrapper
    motor_on_thread = Thread(target=drone_wrapper.motor_on, args=())
    motor_on_thread.start()
    return ""


@app.route("/motor_off", methods=["POST"])
def turn_motor_off():
    global drone_wrapper
    motor_off_thread = Thread(target=drone_wrapper.motor_off, args=())
    motor_off_thread.start()
    return ""


@app.route("/flip", methods=["POST"])
def flip():
    directions = ['l', 'r', 'f', 'b']
    direction = str(request.form["button"])
    print(direction)
    if direction not in directions:
        print('bad direction')
        return ('bad direction')
    global drone_wrapper
    flip_forward_thread = Thread(target=drone_wrapper.flip, args=(direction,))
    flip_forward_thread.start()
    return render_template("control.html", direction=direction)


@app.route("/set_speed", methods=["GET", "POST"])
def set_drone_speed():
    global drone_wrapper
    print('raw speed:', request.form["speedSlider"])
    speed = int(request.form["speedSlider"])
    if speed < 10 or speed > 100:
        print('cant set speed to that amount')
        return 'Bad speed amount'
    set_speed_thread = Thread(target=drone_wrapper.set_speed, args=(speed,))
    set_speed_thread.start()
    return render_template("control.html", speed=speed)


@app.route("/drone_move", methods=["POST"])
def drone_move():
    global drone_wrapper
    direction = str(request.form["button"])
    distance = int(request.form["value"])
    directions = ['up', 'down', 'left', 'right', 'forward', 'back']
    print("Direction: ", direction)
    print("Distance: ", distance)
    if direction not in directions:
        print('bad direction value')
        return 'Bad direction value'
    if distance < 20 or distance > 500:
        print('Cannot set distance to that amount')
        return 'Bad distance value'
    drone_udlr_thread = Thread(target=drone_wrapper.go_up_down_left_right, args=(direction, distance,))
    drone_udlr_thread.start()
    return render_template("control.html", direction=direction, distance=distance)


@app.route("/drone_rotate", methods=["POST"])
def rotate_drone():
    global drone_wrapper
    direction = str(request.form["button"])
    degrees = int(request.form["value"])
    directions = ['cw', 'ccw']
    print("Direction: ", direction)  # print(f"Received: {latest_data} from {addr}")

    print("Degrees: ", degrees)
    if direction not in directions:
        print('bad direction value')
        return 'bad direction value'
    if degrees < 1 or degrees > 360:
        print('cant rotate  to that amount')
        return 'bad degrees value'
    drone_rotate_thread = Thread(target=drone_wrapper.rotate_drone, args=(direction, degrees))
    drone_rotate_thread.start()
    return render_template("control.html", direction=direction, degrees=degrees)


@app.route("/get_tello_data", methods=["GET"])
def get_tello_data():
    global drone_wrapper
    if drone_wrapper is None:
        return 'No data'
    else:
        print('Data:', drone_wrapper.get_drone_state())
        return json.dumps(drone_wrapper.get_drone_state(), indent=4)


@app.route('/get_latest_esp32_data', methods=["GET"])
def get_latest_data():
    global latest_data
    return latest_data


@app.route("/get_drone_coords", methods=["GET"])
def get_drone_coords():
    global drone_wrapper
    if drone_wrapper is None:
        return jsonify({'error': 'No data'})
    else:
        # set this value when the anchors are deployed
        # (-) value if B is to the right of A
        tag_positions = parse_esp32_data.get_tag_location(-2.0828)
        if tag_positions is None:
            return jsonify({'error': 'No tag positions'})
        else:
            x, y = tag_positions
            return jsonify({'x': x, 'y': y})
    # rand_x = random.randint(-5, 5)
    # rand_y = random.randint(-1, 5)
    # return jsonify({'x': rand_x, 'y': rand_y})


# Initialize the Kalman filter
kf = KalmanFilter(dim_x=9, dim_z=2)
kf.x = np.array([0., 0., 0., 0., 0., 0., 0., 0., 0.])
kf.F = np.array([[1., 0., 0., 1., 0., 0., 0., 0., 0.],
                 [0., 1., 0., 0., 1., 0., 0., 0., 0.],
                 [0., 0., 1., 0., 0., 1., 0., 0., 0.],
                 [0., 0., 0., 1., 0., 0., 0., 0., 0.],
                 [0., 0., 0., 0., 1., 0., 0., 0., 0.],
                 [0., 0., 0., 0., 0., 1., 0., 0., 0.],
                 [0., 0., 0., 0., 0., 0., 1., 0., 0.],
                 [0., 0., 0., 0., 0., 0., 0., 1., 0.],
                 [0., 0., 0., 0., 0., 0., 0., 0., 1.]])
kf.H = np.array([[1., 0., 0., 0., 0., 0., 0., 0., 0.],
                 [0., 1., 0., 0., 0., 0., 0., 0., 0.]])
kf.P *= 1000.
kf.R = np.diag([0.1, 0.1])
kf.Q = np.diag([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

# Initialize the state vector and previous pitch, roll, and yaw values
state = np.array([0., 0., 0., 0., 0., 0., 0., 0., 0.])
prev_pitch = 0.
prev_roll = 0.
prev_yaw = 0.
filtered_coords = []


@app.route("/get_filtered_coords", methods=["GET"])
def get_filtered_coords():
    global filtered_coords, kf, prev_yaw, prev_pitch, prev_roll

    esp32_data = requests.get('http://localhost:5000/get_drone_coords').json()

    # Get pitch, roll, yaw, and acceleration data from the /get_tello_data route
    tello_data = requests.get('http://localhost:5000/get_tello_data').json()

    # Extract pitch, roll, yaw, and acceleration values from the received data
    pitch = tello_data['pitch']
    roll = tello_data['roll']
    yaw = tello_data['yaw']
    acceleration_x = tello_data['agx']
    acceleration_y = tello_data['agy']
    acceleration_z = tello_data['agz']
    # Update the state vector with new inputs
    kf.x[6] = pitch - prev_pitch
    kf.x[7] = roll - prev_roll
    kf.x[8] = yaw - prev_yaw

    # Store the previous values for the next iteration
    prev_pitch = pitch
    prev_roll = roll
    prev_yaw = yaw

    # Use the Kalman filter to update the state
    kf.predict()
    if esp32_data is not None:
        z = np.array([[esp32_data['x']], [esp32_data['y']]])
        kf.update(z)

    # Store the latest filtered coordinates
    filtered_coords.append((kf.x[0], kf.x[1]))
    if len(filtered_coords) > 10:
        filtered_coords.pop(0)

    # Return the latest filtered coordinates and additional data
    return jsonify(
        {'filtered_coords': filtered_coords, 'pitch': pitch, 'roll': roll, 'yaw': yaw, 'acceleration_x': acceleration_x,
         'acceleration_y': acceleration_y, 'acceleration_z': acceleration_z})


@app.route("/compare_k_and_real", methods=["GET"])
def compare_kahlman_and_real():
    num_iterations = 10
    total_diff_x = 0
    total_diff_y = 0

    for _ in range(num_iterations):
        # Get the real drone coordinates from the /get_drone_coords endpoint
        real_coords_data = requests.get('http://localhost:5000/get_drone_coords').json()

        # Get the filtered coordinates from the /get_filtered_coords endpoint
        filtered_coords_data = requests.get('http://localhost:5000/get_filtered_coords').json()

        # Extract x and y values from both sets of coordinates
        real_x = real_coords_data['x']
        real_y = real_coords_data['y']
        filtered_x = filtered_coords_data['filtered_coords'][-1][0]
        filtered_y = filtered_coords_data['filtered_coords'][-1][1]

        # Calculate the difference between real and filtered coordinates
        diff_x = abs(real_x - filtered_x)
        diff_y = abs(real_y - filtered_y)

        # Accumulate the differences
        total_diff_x += diff_x
        total_diff_y += diff_y

    # Calculate the average difference
    avg_diff_x = total_diff_x / num_iterations
    avg_diff_y = total_diff_y / num_iterations

    # Return the average difference
    return jsonify({'average_difference': {'x': avg_diff_x, 'y': avg_diff_y}})


class DropLocation:
    def __init__(self, alias, mission_pad, coords):
        self.alias = alias
        self.mission_pad = mission_pad
        self.coords = coords
        coords_dict = json.loads(coords)
        self.x = coords_dict['x']
        self.y = coords_dict['y']

    def get_mission_pad(self):
        return self.mission_pad()


matplotlib.use('Agg')


@app.route("/submit_drop_locations", methods=['POST'])
def submit_drop_locations():
    global drop_locations
    x_values = []
    y_values = []
    aliases = []

    if request.method == 'POST':
        data = request.get_json()

        new_drop_locations = []  # create a new list to hold the new data

        for location in data:
            drop_location = DropLocation(location['alias'], location['mission_pad'], location['coords'])
            new_drop_locations.append(drop_location)

        drop_locations = new_drop_locations  # overwrite existing drop_locations with new data

        chart_data = []

        for loc in drop_locations:
            chart_data.append({
                'x': loc.x,
                'y': loc.y,
                'alias': loc.alias
            })

        return jsonify(chart_data)
    else:
        return 'Invalid request method'


@app.route("/get_drop_locations", methods=['GET'])
def get_drop_locations():
    global drop_locations

    data = []

    for location in drop_locations:
        coords_dict = json.loads(location.coords)  # convert coords string to a dictionary
        data.append({
            'alias': location.alias,
            'mission_pad': location.mission_pad,
            'coords': coords_dict
        })

    return jsonify(data)


@app.route("/pathfind", methods=['POST'])
def pathfind():
    # take in src and a dst from the endpoint containing the current instruction
    data = request.json

    success = False

    def execute_flight_plan():
        nonlocal success
        try:
            # do our tello movements here
            global drone_wrapper
            takeoff_thread = Thread(target=drone_wrapper.takeoff, args=())
            takeoff_thread.start()
            time.sleep(4)

            detected_dest_mission_pad = False
            mpad_counter = 0
            while not detected_dest_mission_pad:
                if mpad_counter > 9:
                    detected_dist_mission_pad = True
                else:
                    if drone_wrapper.get_mission_pad() == dst_mpad:
                        mpad_counter += 1

                curr_x, curr_y = where_is_tag_stats()
                distance, angle, direction = helpers.calculate_distance_angle(curr_x, curr_y, dst_x, dst_y)

                while distance > .2:
                    curr_x, curr_y = where_is_tag_stats()
                    distance, angle, direction = helpers.calculate_distance_angle(curr_x, curr_y, dst_x, dst_y)
                    drone_wrapper.rotate_drone('cw', angle)

                    print('rotated the drone')
                    time.sleep(2)
                    drone_wrapper.emergency()

                drone_wrapper.land()
                return

            drone_wrapper.emergency()

            success = True
        except Exception as e:
            print("An error occurred during flight plan execution:", e)
            success = False
            error_message = str(e)
            response_data = {'error': error_message, 'instruction_number': number}
            return response_data

        # Create a new thread to execute the flight plan
        t = Thread(target=execute_flight_plan)
        t.start()

        # Wait for the thread to finish executing
        t.join()

        # Return a response based on the success or failure of the operation
        if success:
            # Return a success response if the operation was successful
            response_data = {'status': 'success', 'instruction_number': number}
            status_code = 200

        else:
            # Return an error response if the operation failed
            response_data = {'error': 'Failed to execute flight plan', 'instruction_number': number}
            status_code = 500

        response = jsonify(response_data)
        response.status_code = status_code

        # return the response object with the status code
        return response


import helpers
import statistics


def where_is_tag_stats():
    # Initialize lists to store the values
    x = []
    y = []
    for i in range(10):
        esp32_data = requests.get('http://localhost:5000/get_drone_coords').json()
        x_loc = esp32_data['x']
        x.append(x_loc)
        y_loc = esp32_data['y']
        y.append(y_loc)
        time.sleep(0.1)

    # Filter out the outliers using the median absolute deviation (MAD) method
    med_x = statistics.median(x)
    med_y = statistics.median(y)
    mad_x = statistics.median([abs(d - med_x) for d in x])
    mad_y = statistics.median([abs(a - med_y) for a in y])
    filtered_x = [d for d in x if abs(d - med_x) < 3 * mad_x]
    filtered_y = [a for a in y if abs(a - med_y) < 3 * mad_y]

    # Calculate the average value
    avg_x = statistics.mean(filtered_x)
    avg_y = statistics.mean(filtered_y)

    # Print the results
    print("Average x:", avg_x)
    print("Average y:", avg_y)
    return avg_x, avg_y


@app.route("/start_drone_mission", methods=['POST'])
def start_drone_mission():
    # Get the flight plan from the /get_flight_plan endpoint
    response = requests.get("http://127.0.0.1:5000/get_flight_plan")

    # Check if the request was successful and load the JSON data
    if response.status_code == 200:
        flight_plan_data = response.json()

        for instruction in flight_plan_data:
            src = instruction['src']
            dst = instruction['dst']
            instruction_number = instruction['instruction_number']
            # grab the coords for the src and dst
            global drop_locations
            dst_x, dst_y, dst_mpad = None, None, None
            src_x, src_y, src_mpad = None, None, None
            for loc in drop_locations:
                if loc.alias == src:
                    src_x, src_y = loc.x, loc.y
                    src_mpad = loc.mission_pad
                if loc.alias == dst:
                    dst_x, dst_y = loc.x, loc.y
                    dst_mpad = loc.mission_pad

            if dst_x is not None and dst_y is not None:
                print('src x:{} y:{}'.format(src_x, src_y))
                print('dst x{} y{}'.format(dst_x, dst_y))
            else:
                # Handle the case where dst was not found
                print('Destination not found')


            try:
                # do our tello movements here
                global drone_wrapper
                print('taking off')
                takeoff_thread = Thread(target=drone_wrapper.takeoff, args=())
                takeoff_thread.start()
                time.sleep(4)

                print('here***')

                # curr_x, curr_y = where_is_tag_stats()
                esp32_data = requests.get('http://localhost:5000/get_drone_coords').json()
                curr_x = esp32_data['x']
                curr_y = esp32_data['y']

                distance, angle, direction = helpers.calculate_distance_angle(curr_x, curr_y, dst_x, dst_y)
                print('distance:', distance)
                print('angle:', angle)

                drone_wrapper.rotate_drone('cw', angle)
                print('rotated the drone')
                time.sleep(2)

                # go forward
                amount = (distance*100)/2
                drone_wrapper.go_up_down_left_right('forward', amount)
                time.sleep(2)

                drone_wrapper.land()

            except Exception as e:
                print('Exception', e)

        return jsonify(flight_plan_data)  # Return flight plan data as JSON

    else:
        return jsonify({"error": "Failed to retrieve flight plan data."}), 500

import time
import requests
import json
import cmath
import matplotlib.pyplot as plt
import requests
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

distance_a1_a2 = 1.524
window_size = 60  # Show the last 10 seconds of data


# Create lists to store the x and y coordinates of the tag position

def parse_esp_32_data():
    response = requests.get('http://127.0.0.1:5000/get_latest_esp32_data')
    if response.text:
        data = json.loads(response.text)
    else:
        data = {}  # or any default value you want to use when the response is empty

    # Extract the "A" and "R" values for each link
    dist_a = None
    dist_b = None
    try:
        for link in data['links']:
            if link['A'] == '1A86':
                dist_a = float(link['R'])
            elif link['A'] == '1B86':
                dist_b = float(link['R'])
    except KeyError:
        dist_a = 0
        dist_b = 0
    # Print the extracted values
    print('dist_a: {} - dist_b: {}'.format(dist_a, dist_b))
    return dist_a, dist_b


import time
import requests
import json
import cmath
import matplotlib.pyplot as plt


def collect_and_plot_distances(duration=60, interval=0.1, expected_value_a=0, expected_value_b=0):
    # Create empty lists to store the distances over time
    dist_a_history = []
    dist_b_history = []

    # Set up the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # Set the x and y limits for both subplots
    xlim = (0, duration)
    ylim = (0, 10)
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)

    # Record the start time of the data collection
    start_time = time.time()

    # Continuously retrieve and plot the distances for the duration of the data collection
    while time.time() - start_time <= duration:
        # Get the latest distances from the ESP32
        dist_a, dist_b = parse_esp_32_data()

        # Convert the distances from meters to feet
        try:
            dist_a_ft = dist_a * 3.28084
            dist_b_ft = dist_b * 3.28084
        except TypeError as e:
            if dist_a is None:
                dist_a_ft = 0 * 3.28084
            if dist_b is None:
                dist_b_ft = 0 * 3.28084
            continue

        # Add the distances to the history lists
        dist_a_history.append(dist_a_ft)
        dist_b_history.append(dist_b_ft)

        # Clear the previous plot and plot the history of distances for anchor A
        ax1.clear()
        ax1.scatter([i * interval for i in range(len(dist_a_history))], dist_a_history, label='Distance to Anchor A')
        ax1.legend()
        ax1.set_title('Distance to Anchors A and B over Time')
        ax1.set_ylabel('Distance (ft)')
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)

        # Clear the previous plot and plot the history of distances for anchor B
        ax2.clear()
        ax2.scatter([i * interval for i in range(len(dist_b_history))], dist_b_history, label='Distance to Anchor B')
        ax2.legend()
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Distance (ft)')
        ax2.set_xlim(xlim)
        ax2.set_ylim(ylim)

        # Draw the plot
        plt.draw()

        # Show the plot without blocking the code
        plt.show(block=False)

        # Wait for the time interval before retrieving the next set of distances
        time.sleep(interval)

    # Show the final plot after the data collection is complete
    plt.show()

    # Print the collected distances
    print('Distance to Anchor A over time: {}'.format(dist_a_history))
    print('Distance to Anchor B over time: {}'.format(dist_b_history))

    # Calculate the mean of the collected distances for anchor A and B
    mean_dist_a = sum(dist_a_history) / len(dist_a_history)
    mean_dist_b = sum(dist_b_history) / len(dist_b_history)

    # Create lists of the expected values based on the mean distances to anchors A and B
    expected_values_a = [expected_value_a] * len(dist_a_history)
    expected_values_b = [expected_value_b] * len(dist_b_history)

    # Plot the expected vs real distances for anchor A
    fig, ax = plt.subplots()
    ax.plot([i * interval for i in range(len(dist_a_history))], expected_values_a,
            label='Expected Distance to Anchor A')
    ax.plot([i * interval for i in range(len(dist_a_history))], dist_a_history, label='Actual Distance to Anchor A')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (ft)')
    ax.set_title('Expected vs Actual Distance to Anchor A over Time')
    ax.legend()
    plt.show()

    # Plot the expected vs real distances for anchor B
    fig, ax = plt.subplots()
    ax.plot([i * interval for i in range(len(dist_b_history))], expected_values_b,
            label='Expected Distance to Anchor B')
    ax.plot([i * interval for i in range(len(dist_b_history))], dist_b_history, label='Actual Distance to Anchor B')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (ft)')
    ax.set_title('Expected vs Actual Distance to Anchor B over Time')
    ax.legend()
    plt.show()


from math import acos, cos, sin, radians, sqrt


def calculate_tag_location(dist_a, dist_b, dist_c):
    # Coordinates of anchors A and B
    a_x, a_y = 0, 0
    b_x, b_y = 3, 0

    # Calculate the cosine and sine of angle A using the law of cosines
    cos_a = (dist_b ** 2 + dist_c ** 2 - dist_a ** 2) / (2 * dist_b * dist_c)
    if abs(cos_a) > 1:
        # Handle rounding errors that may cause cos_a to be outside the valid range
        sin_a = 0
    else:
        sin_a = sqrt(1 - cos_a ** 2)

    # Calculate the x and y coordinates of the tag
    x = dist_b * cos_a
    y = dist_b * sin_a

    # Determine the signs of the distances
    dist_a_sign = 1 if dist_a >= 0 else -1
    dist_b_sign = 1 if dist_b >= 0 else -1

    # Adjust the signs of the coordinates if necessary
    if dist_a_sign != dist_b_sign and y < 0:
        x = -x
        y = -y

    # Subtract the distance c to make anchor A the origin
    x -= dist_c

    # Add the coordinates of anchor A to get the absolute coordinates of the tag
    x_t = a_x + x
    y_t = a_y + y

    # Return the tag coordinates as a tuple
    return x_t, y_t


def get_tag_location(distance_a_b):
    try:
        dist_a, dist_b = parse_esp_32_data()
        tag_location = calculate_tag_location(dist_a, dist_b, distance_a_b)
        print('Tag location: ({}, {})'.format(tag_location[0], tag_location[1]))
        return tag_location
    except TypeError:
        print('Error: One or both of the distances is None.')
        return None


def collect_and_plot_coordinates(interval, distance_a_b):
    # Initialize empty lists to store the x and y coordinates
    x_coords = []
    y_coords = []

    # Calculate the known distance value between the anchors
    c = 3.0  # Replace with your actual distance value

    # Initialize the plot
    fig, ax = plt.subplots()
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_xticks(range(-10, 11))
    ax.set_yticks(range(-10, 11))
    ax.grid(True)
    ax.set_xlabel('Distance from Anchor A (m)')
    ax.set_ylabel('Distance from Anchor A (m)')

    # Add label 'A' at (0, 0)
    ax.text(0, 0, 'A', fontsize=12, color='red', ha='center', va='center')

    # Add point 'B' at (-3, 0) and label it
    ax.scatter(-3, 0, s=150, color='green', marker='o')
    ax.text(-3, 0, 'B', fontsize=12, color='green', ha='center', va='center')

    # Collect data and plot each point separately
    while True:
        dist_a, dist_b = parse_esp_32_data()
        x, y = calculate_tag_location(dist_a, dist_b, distance_a_b)
        print('Relative (x,y):({},{})'.format(x, y))
        x_coords.append(x)
        y_coords.append(y)
        ax.scatter(x, y)
        plt.pause(interval)

    # Show the final plot
    plt.show()

# Call the function to collect and plot x and y coordinates separately for 1 minute with a sampling interval of 0.1
# seconds
# collect_and_plot_coordinates(interval=0.1, distance_a_b=1.6764)

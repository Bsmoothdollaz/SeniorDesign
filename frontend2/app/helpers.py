# from location import location
import math


def validate_location_instruction(instruction):
    locations = ['Home', 'A', 'B', 'C']
    # print('validate location:', instruction)
    parsed = instruction.split('->')
    if len(parsed) > 1:
        start = parsed[0]
        end = parsed[1]
        if start not in locations or end not in locations:
            print('REFERENCED A LOCATION THAT DOESNT EXIST!')
    return True


def validate_drone_instruction(instruction):
    drone_instruction_identifier = instruction[0]
    rest_of_instruction = instruction[1:].strip()
    if rest_of_instruction not in ['pickup food_2', 'pickup food_1', 'pickup food_3',
                                   'drop food_2', 'drop food_1', 'drop food_3']:
        raise Exception('Not a valid drone instruction!')
    return True


def backend_validate_flight_plan(text):
    if len(text) == 0:
        return 'No text provided'
    else:
        converted_text = text.strip()
        list_of_instructions = converted_text.split(';')
        err_counter = 0

        # validate our flight plan
        # we need to add an identifier "start" at the beginning
        # we need to and "end"
        # start needs to match end

        for instruction in list_of_instructions:
            if len(instruction) > 0:
                if '*' in instruction:
                    try:
                        validate_drone_instruction(instruction)
                    except Exception as e:
                        print(e)
                        return e
                else:
                    try:
                        validate_location_instruction(instruction)
                    except Exception as e:
                        print(e)
                        return e

        print('Validated Successfully!')
    print('validated')


def backend_submit_flight_plan(text):
    if len(text) == 0:
        return 'No text provided'
    else:
        converted_text = text.strip()
    print('submitted')


def get_connection_status():
    print('THREAD')
    return True


def get_tello_status():
    return '10'


#
# example = '*pickup food_2;Home->B;*drop food_2;A->Home;'
#
# backend_validate_flight_plan(example)

def calculate_distance_angle(src_x, src_y, dst_x, dst_y):
    # Calculate distance from home to point
    distance = math.sqrt((dst_x - src_x) ** 2 + (dst_y - src_y) ** 2)

    # Calculate angle from home to point
    dx = dst_x - src_x
    dy = dst_y - src_y

    quadrant_num = -1
    direction = 'cw'

    if dx == 0:
        if dy > 0:
            # needs to rotate 0 degrees
            quadrant_num = -1
            temp_angle = 0
        elif dy < 0:
            # needs to rotate 180 degrees
            quadrant_num = -1
            temp_angle = 180
        else:
            # needs to rotate 0 degrees
            quadrant_num = -1
            temp_angle = 0
    elif dy == 0:
        if dx > 0:
            # needs to rotate 90 degrees cw
            quadrant_num = -1
            temp_angle = 90
        elif dx < 0:
            # needs to rotate 270 degrees cw
            quadrant_num = -1
            temp_angle = 270
        else:
            # needs to rotate 0 degrees
            quadrant_num = -1
            temp_angle = 0
    else:
        angle = math.degrees(math.atan2(dy, dx))

        if angle < 0:
            angle += 360

        # Calculate the direction of the angle based on the x and y values
        if dx > 0 and dy >= 0:
            quadrant_num = 1
        elif dx <= 0 and dy > 0:
            quadrant_num = 2
        elif dx < 0 and dy <= 0:
            quadrant_num = 3
        elif dx >= 0 and dy < 0:
            quadrant_num = 4

        print('quadrant number: {}'.format(quadrant_num))

        temp_angle = -1
        if quadrant_num == 1:
            temp_angle = 90 - angle
        elif quadrant_num == 2:
            temp_angle = 180 + angle
        elif quadrant_num == 3:
            temp_angle = (270 - angle) + 180
        elif quadrant_num == 4:
            temp_angle = (360 - angle) + 90

        print('temp_angle', temp_angle)
    return distance, temp_angle, direction

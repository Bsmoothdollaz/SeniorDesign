# from location import location


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

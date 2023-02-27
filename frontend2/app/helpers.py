def backend_validate_flight_plan(text):
    if len(text) == 0:
        return 'No text provided'
    else:
        converted_text = text.strip()
    print('validated')


def backend_submit_flight_plan(text):
    if len(text) == 0:
        return 'No text provided'
    else:
        converted_text = text.strip()
    print('submitted')

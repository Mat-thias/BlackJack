"""
This is a module with a list of functions for input handling
"""


def get_input_str_from_choice(choices, input_message, error_message=None, case_sensitive=False):
    """
    Gets a string in put from a list of choices.
    choices: the list of valid string inputs
    input_message: the input message to be displayed as the input prompt
    error_message: the input message to be displayed as the input prompt when an invalid input is entered
    case_sensitive: default to False, set to True if you want the input to match the choice with case
    return: a string in the choice the user inputs
    """
    input_str = input(input_message)
    if error_message is None:
        error_message = "Not a valid choice : "
    if case_sensitive:
        while input_str not in choices:
            input_str = input(error_message)
    else:
        choices = list(map(lambda x: x.upper(), choices))
        while input_str.upper() not in choices:
            input_str = input(error_message)

    return input_str


def get_input_int(input_message, error_massage=None, input_range=None):
    """
    Gets a valid integer within a specific range if specified by input_range else just a valid integer
    input_message: the input message to be displayed as the input prompt
    error_message: the input message to be displayed as the input prompt when an invalid input is entered
    input_range: the range of valid integers the user can input, best to be specified by range
    return: a valid integer within the input_range if specified else just a valid integer
    """
    input_str = input(input_message)
    if error_massage is None:
        error_massage = "Input should be a valid integer : "
    while True:
        try:
            input_int = int(input_str)
            if range and input_int in input_range:
                return input_int
        except ValueError:
            input_str = input(error_massage)
        else:
            input_str = input(error_massage)


def get_input_float(input_message, error_massage=None, upper_limit=None, lower_limit=None):
    """
    Gets a valid float within a specific range specified by the upper_limit and lower_limit
    input_message: the input message to be displayed as the input prompt
    error_message: the input message to be displayed as the input prompt when an invalid input is entered
    upper_limit: the user input must be less than this value, if not specified then no upper limit is restricted
    lower_limit: the user input must be greater than this value, if not specified then no lower limit is restricted
    return: a valid float within the range specifies by the upper_limit and lower_limit if specified
        else just a valid float
    """
    input_str = input(input_message)
    if error_massage is None:
        error_massage = f"Input should be a valid floating number" \
                        f" not less then {lower_limit} and not greater then {upper_limit} : "
    while True:
        try:
            input_float = float(input_str)
            if (upper_limit is not None and input_float <= upper_limit)\
                    and (lower_limit is not None and input_float >= lower_limit):
                return input_float
        except ValueError:
            input_str = input(error_massage)
        else:
            input_str = input(error_massage)

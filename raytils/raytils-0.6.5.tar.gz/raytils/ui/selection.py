from collections.abc import Hashable
from ast import literal_eval
from typing import Dict, Union, Any, Iterable, Sized, Type

from raytils.ui.formatting import suffix_join

try:
    input = raw_input
except NameError:
    pass


def get_string_type(input_data: str) -> Type:
    """Returns the type of a string by evaluating it"""
    try:
        return type(literal_eval(input_data))
    except (ValueError, SyntaxError):
        return str


def get_input(prompt: str = "", true_type: bool = False) -> Any:
    """Returns input from the user and optionally converts it to the appropriate python type"""
    response = input(prompt)

    if true_type:
        string_type = get_string_type(response)
        return string_type(response)

    return response


def get_selection_from_dict(options: Dict[Union[str, int, float], Any], required: bool = True) -> Any:
    """Prompts the user for a choice from a given selection of dict values using their keys as the selectors

    Args:
        options: A dictionary of options (values) and selectors (keys)
        required: If true the function will not return until a valid selection is made, if false it can return None

    Returns:
        A value from the options dictionary or possibly None if required is False
    """
    prompt = "Enter Selection: "
    valid_selection = False
    selection = 0

    options_string = "Options: \n\t" + '\n\t'.join(["{}: {}".format(k, v) for k, v in options.items()])
    print(options_string)

    while not valid_selection:
        selection = get_input(prompt, true_type=True)
        if not isinstance(selection, Hashable) or selection not in options:
            if not required:
                return None
            valid_options = suffix_join((["{} ({})".format(k, str(type(k))) for k in options.keys()]), ', ', ' or ')
            print("'{}' ({}) is not a valid option, please choose from: {}".format(selection, type(selection),
                                                                                   valid_options))
            continue
        valid_selection = True

    return options[selection]


def get_selection_from_list(options: list, required: bool = True) -> Any:
    """Prompts the user for a choice from a given selection of list values using integers as selection options

    Args:
        options: A list of options for selection
        required: If true the function will not return until a valid selection is made, if false it can return None

    Returns:
        A value from the options list or possibly None if required is False
    """
    return get_selection_from_dict({i: v for i, v in enumerate(options)}, required)


def __test_selections():
    test_options_list = ["Selection Zero", "Two"]
    test_options_dict = {1.2: 1.2, "Zero": "Selection Zero", 2: "Two"}
    selection = get_selection_from_dict(test_options_dict)
    print("Selected:", selection)
    selection = get_selection_from_list(test_options_list)
    print("Selected:", selection)
    selection = get_selection_from_list(test_options_list, required=False)
    print("Selected:", selection)



if __name__ == '__main__':
    __test_selections()

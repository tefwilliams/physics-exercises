import importlib
from typing import Callable


def get_full_module_name(module_name: str):
    match module_name:
        case "np":
            return "numpy"

        case "pd":
            return "pandas"

        case _:
            return module_name


def get_from_module(input_string: str):
    try:
        module_name, attribute_name = input_string.split(".")

    except ValueError:
        raise ValueError(f"{input_string} is not in module.attribute format")

    full_module_name = get_full_module_name(module_name)
    module = importlib.import_module(full_module_name)

    return module.__getattribute__(attribute_name)


def get_function(choice: str):
    try:
        func = eval(choice)

    except NameError:
        try:
            func = get_from_module(choice)

        except Exception as e:
            raise ValueError(e)

    if not callable(func):
        raise ValueError("\n" + f"'{choice}' is not a defined function")

    return func


def get_1d_function(input_string: str) -> Callable[[float], float]:
    """
    Attempts to get a valid function from the input string
    Has access to math, numpy (as np), and pandas (as pd)
    """
    func = get_function(input_string)

    try:
        # Confirm a call with a number returns a float
        assert isinstance(func(0.0), float)

    except:
        raise ValueError(
            "\n"
            + f"'{input_string}' does not have the required shape: f(float) -> float"
        )

    return func


def input_positive_int(input_string: str):
    while True:
        choice = input_int(input_string)

        if choice >= 1:
            return choice

        print(f"{choice} is less than 1")


def input_int(input_string: str):
    while True:
        choice = input(input_string)

        try:
            return int(choice)

        except ValueError:
            print(f"{choice} is not a valid integer")


def input_float(input_string: str):
    while True:
        choice = input(input_string)

        try:
            return float(choice)

        except ValueError:
            try:
                module_item = get_from_module(choice)

                try:
                    return float(module_item)

                except:
                    print(f"{choice} is not a valid number")

            except Exception as e:
                print(e)

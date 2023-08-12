from typing import Callable


def get_function(input_string: str) -> Callable[[float], float]:
    """
    Attempts to get a valid function from the input string
    Has access to math, numpy (as np), and pandas (as pd)
    """
    if input_string.startswith("np"):
        import numpy as np
    if input_string.startswith("pd"):
        import pandas as pd
    if input_string.startswith("math"):
        import math

    try:
        choice = eval(input_string)
        # Confirm a call with a number returns a float
        float(choice(0))
        return choice

    except (NameError, AttributeError):
        raise ValueError("\n" + f"'{input_string}' is not a defined function")


def input_positive_int(input_str):
    while True:
        choice = input_int(input_str)

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
            print(f"{choice} is not a valid number")

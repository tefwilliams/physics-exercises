from typing import Callable
from .module_helpers import get_from_module


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

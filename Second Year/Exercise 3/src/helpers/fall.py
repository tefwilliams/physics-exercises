from typing import Callable
from physics_exercise_helpers import (
    get_comma_separated_string,
    input_float,
    input_positive_float,
)
from .physics_helpers import get_acceleration
from .plot_helpers import plot_fall
from .methods import MethodString, iterate


def run_fall(air_density: Callable[[float], float]):
    initial_height = 10000
    initial_velocity = 0
    time_step = 0.1

    methods = [
        MethodString.EULER,
        MethodString.MODIFIED_EULER,
        MethodString.RUNGE_KUTTA,
    ]

    while True:
        choice = input(
            f"""
Select one of the following options:
'r': To run the {get_comma_separated_string(method.value for method in methods)} methods with the parameters:
    initial height: {initial_height}s
    initial vertical velocity: {initial_velocity}m/s
    time step: {time_step}s
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print(f"\nYou entered the choice: '{choice}'")

        match choice:
            case "r":
                plot_fall(
                    {
                        method.value: iterate(
                            initial_height,
                            initial_velocity,
                            get_acceleration,
                            air_density,
                            method.to_method(),
                            time_step,
                        )
                        for method in methods
                    }
                )

            case "m":
                initial_height = input_positive_float(
                    "Enter a value for the initial height: "
                )
                initial_velocity = input_float(
                    "Enter a value for the initial velocity: "
                )
                time_step = input_positive_float("Enter a value for the time step: ")

            case "q":
                break

            case _:
                print("\nThis is not a valid choice")

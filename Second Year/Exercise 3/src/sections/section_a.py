import numpy as np
from helpers import (
    get_comma_separated_string,
    input_float,
    input_positive_float,
    plot_fall,
)
from helpers import MethodString, IterationData, iterate


def run():
    print("\nYou have chosen part (a)")

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
'r': To run the {get_comma_separated_string(methods)} methods with the parameters:
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


def get_acceleration(velocity: float, height: float):
    gravitational_constant = 9.81

    return get_drag(velocity, height) - gravitational_constant


def get_drag(velocity: float, height: float):
    drag_coefficient = 0.6
    air_density = lambda height: 1.2 * np.e ** (-height / 10400)
    area = 1
    mass = 100

    return -(
        drag_coefficient * air_density(height) * area * abs(velocity) * velocity
    ) / (2 * mass)

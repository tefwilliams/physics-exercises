from enum import StrEnum
import matplotlib.pyplot as plt
import numpy as np

from methods import MethodString, iterate


def run():
    print("\n" + "You have chosen part (a)")

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
            "\n"
            + f"""Select one of the following options:
'r': To run the {get_comma_separated_string(methods)} methods with the parameters:
    initial height: {initial_height}s
    initial vertical velocity: {initial_velocity}m/s
    time step: {time_step}s
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "r":
                plot_comparison(methods, initial_height, initial_velocity, time_step)

            case "m":
                # lower_bound = input_float("Enter a value for the lower bound: ")
                # upper_bound = input_float("Enter a value for the upper bound: ")
                # number_of_steps = input_positive_int(
                #     "Enter a value for the number of steps: "
                # )
                print("Hello")

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")


def plot_comparison(
    methods: list[MethodString],
    initial_height: float,
    initial_velocity: float,
    time_step: float,
):
    for method in methods:
        (
            acceleration_record,
            velocity_record,
            height_record,
            time_record,
        ) = iterate(
            initial_height,
            initial_velocity,
            get_acceleration,
            method.to_method(),
            time_step,
        )

        plt.plot(time_record, height_record)
    plt.show()


def get_comma_separated_string(strings: list[str | StrEnum]):
    return (
        strings[0]
        if len(strings) == 1
        else f"{', '.join(strings[:-1])}, and {strings[-1]}"
    )


def get_acceleration(velocity: float, height: float):
    gravitational_constant = 9.81

    return get_drag(velocity, height) - gravitational_constant


def get_drag(velocity: float, height: float):
    drag_coefficient = 0.6
    # air_density = lambda height: 1.2
    air_density = lambda height: 1.2 * np.e ** (-height / 10400)
    area = 1
    mass = 100

    return -(
        drag_coefficient * air_density(height) * area * abs(velocity) * velocity
    ) / (2 * mass)


run()

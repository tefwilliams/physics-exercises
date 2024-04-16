from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
from helpers import (
    get_comma_separated_string,
    input_positive_float,
    input_float,
    iterate,
    MethodString,
    IterationData,
)

gravitational_constant = -9.81
mass = 100
drag_coefficient = 0.6


def run():
    print("\nYou have chosen part (b)")

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

                data = {
                    method.value: iterate(
                        initial_height,
                        initial_velocity,
                        get_acceleration,
                        method.to_method(),
                        time_step,
                    )
                    for method in methods
                }

                time_steps = data[MethodString.EULER]["time"]

                plot_differences(
                    data,
                    {
                        "acceleration": get_analytical_acceleration(time_steps),
                        "velocity": get_analytical_velocity(time_steps),
                        "height": get_analytical_height(initial_height, time_steps),
                        "time": time_steps,
                    },
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
                print("\n" + "This is not a valid choice")


def plot_differences(
    data: dict[str, IterationData],
    true_data: IterationData,
):
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
    ax1: Axes = axes[0]
    ax2: Axes = axes[1]
    ax3: Axes = axes[2]

    for records in data.values():
        ax1.plot(records["time"], sub_list(records["height"], true_data["height"]))
        ax2.plot(
            records["time"],
            sub_list(records["velocity"], true_data["velocity"]),
        )
        ax3.plot(
            records["time"],
            sub_list(records["acceleration"], true_data["acceleration"]),
        )

    ax1.set_ylabel("Height Difference ($m$)")
    ax2.set_ylabel("Velocity Difference ($ms^{-1}$)")
    ax3.set_ylabel("Acceleration Difference ($ms^{-2}$)")
    ax3.set_xlabel("Time ($s$)")
    fig.legend(data.keys())

    fig.show()


def sub_list(list1: list[float], list2: list[float]):
    return [item1 - item2 for item1, item2 in zip(list1, list2)]


def get_acceleration(velocity: float, height: float):
    return gravitational_constant + get_drag(velocity, height)


def get_drag(velocity: float, height: float):
    air_density = lambda _: 1
    area = 1

    return -(
        drag_coefficient * air_density(height) * area * abs(velocity) * velocity
    ) / (2 * mass)


def get_analytical_acceleration(time_steps: list[float]):
    return [gravitational_constant] * len(time_steps)


def get_analytical_velocity(time_steps: list[float]):
    direction = gravitational_constant / abs(gravitational_constant)
    return [
        direction
        * (mass * abs(gravitational_constant) / drag_coefficient) ** 0.5
        * np.tanh((drag_coefficient * abs(gravitational_constant) / mass) ** 0.5 * time)
        for time in time_steps
    ]


def get_analytical_height(initial_height: float, time_steps: list[float]):
    direction = gravitational_constant / abs(gravitational_constant)
    return [
        initial_height
        + (
            direction
            * (mass / (2 * drag_coefficient))
            * np.log(
                np.cosh((drag_coefficient * gravitational_constant / mass**0.5 * time))
                ** 2
            )
        )
        for time in time_steps
    ]

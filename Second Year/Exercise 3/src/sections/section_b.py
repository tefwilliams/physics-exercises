from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
from helpers import get_comma_separated_string
from methods import MethodString, iterate


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

                plot_differences(
                    {
                        method: iterate(
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


def plot_differences(
    data: dict[str, dict[str, list[float]]],
    true_data: dict[str, dict[str, list[float]]],
):
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
    ax1: Axes = axes[0]
    ax2: Axes = axes[1]
    ax3: Axes = axes[2]

    for method, records in data.items():
        true_values = true_data[method]

        ax1.plot(
            records["time"], get_differences(records["height"], true_values["height"])
        )
        ax2.plot(
            records["time"],
            get_differences(records["velocity"], true_values["velocity"]),
        )
        ax3.plot(
            records["time"],
            get_differences(records["acceleration"], true_values["acceleration"]),
        )

    ax1.set_ylabel("Height Difference ($m$)")
    ax2.set_ylabel("Velocity Difference ($ms^{-1}$)")
    ax3.set_ylabel("Acceleration Difference ($ms^{-2}$)")
    ax3.set_xlabel("Time ($s$)")
    fig.legend(data.keys())

    fig.show()


def get_differences(list1: list[float], list2: list[float]):
    assert len(list1) == len(list2)
    return [item1 - list2[i] for i, item1 in enumerate(list1)]


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

import numpy as np
from time import time
from matplotlib import pyplot as plt
from physics_exercise_helpers import input_float, input_positive_int
from helpers import simpson_integrate, mysin, mycos


def plot_intensity(
    w_min: float, w_max: float, number_of_points: int, number_of_steps: int
):
    # Use Simpson's integration and time the calculation

    xvals = np.linspace(w_min, w_max, number_of_points)

    f = np.vectorize(
        lambda x: (
            (simpson_integrate(mysin, 0, x, number_of_steps) + 0.5) ** 2
            + (simpson_integrate(mycos, 0, x, number_of_steps) + 0.5) ** 2
        )
        / 2
    )

    start = time()
    yvals = f(xvals)
    end = time()

    print("\n" + f"The calculation took {end - start:.2f} seconds.")

    # Creates plot with x-limits defined as w min to w max and labels axes

    plt.plot(xvals, yvals)
    plt.title("Intensity at P")
    plt.xlim([w_min, w_max])
    plt.locator_params(axis="y", nbins=5)
    plt.locator_params(axis="x", nbins=5)
    plt.xlabel("$w$")
    plt.ylabel("$I(w)/I_0$")
    plt.show()


def run():
    print("\n" + "You have chosen part (c)")

    w_min = -5
    w_max = 10

    number_of_points = 2000
    number_of_steps = 200

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
'r': To run the section with the following parameters:
    w min: {w_min}
    w max: {w_max}
    number of points: {number_of_points}
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "r":
                plot_intensity(w_min, w_max, number_of_points, number_of_steps)

            case "m":
                w_min = input_float("Enter a value for w min: ")
                w_max = input_float("Enter a value for w max: ")
                number_of_points = input_positive_int(
                    "Enter a value for the number of points: "
                )
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")

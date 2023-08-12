from typing import Callable
import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate

from input_helpers import get_function, input_float, input_positive_int
from integration import simpson_integrate


def run():
    print("\n" + "You have chosen part (d)")

    lower_bound = 0
    upper_bound = 1
    number_of_steps = 100

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
Enter a function for which the convergence of Simpson's rule will be tested, with the following parameters:
    lower bound: {lower_bound}
    upper bound: {upper_bound}
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: {choice}")

        match choice:
            case "m":
                lower_bound = input_float("Enter a value for the lower bound: ")
                upper_bound = input_float("Enter a value for the upper bound: ")
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )

            case "q":
                break

            case _:
                try:
                    function = get_function(choice)

                    x = np.arange(2, number_of_steps + 1, 2)
                    f = np.vectorize(
                        lambda n: simpson_integrate(
                            function, lower_bound, upper_bound, n
                        )
                    )

                    y_simpson = f(x)
                    y_true = integrate.quad(function, lower_bound, upper_bound)[0]

                    # Plots the diff between the Simpson integral value and the 'true' value
                    # for different numbers of steps

                    plt.plot(x, y_simpson - y_true)
                    plt.title("Convergence of the 1D Simpson rule")
                    plt.xlabel("$N$")
                    plt.ylabel(f"Error in integral of {choice}")
                    plt.show()

                except ValueError as e:
                    print(e)

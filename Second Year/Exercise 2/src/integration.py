from typing import Callable
import numpy as np


def simpson_integrate(
    function: Callable[[float], float],
    lower_bound: float,
    upper_bound: float,
    number_of_steps: int,
) -> float:
    "This is the orginial Simpson's rule function"
    step_size = (upper_bound - lower_bound) / number_of_steps

    x = np.linspace(lower_bound, upper_bound, number_of_steps)
    y = np.vectorize(function)(x)

    odds = np.sum(y[1:-1:2])
    evens = np.sum(y[2:-1:2])

    return (step_size / 3) * (y[0] + 4 * odds + 2 * evens + y[-1])

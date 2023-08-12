import numpy as np


class InputStrings:
    N = "Input a value for N: "
    w = "Input a value for the number of points for w: "
    xy = "Input a value for the number of points in the x and y directions: "
    wavelength = "Input a wavelength in micrometers: "


def mysin(x: float) -> float:
    "The sine function for the Fresnel integral"
    return np.sin((np.pi * (x**2)) / 2)


def mycos(x: float) -> float:
    "The cosine function for the Fresnel integral"
    return np.cos((np.pi * (x**2)) / 2)

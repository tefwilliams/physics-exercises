import numpy as np


def mysin(x: float) -> float:
    "The sine function for the Fresnel integral"
    return np.sin((np.pi * (x**2)) / 2)


def mycos(x: float) -> float:
    "The cosine function for the Fresnel integral"
    return np.cos((np.pi * (x**2)) / 2)

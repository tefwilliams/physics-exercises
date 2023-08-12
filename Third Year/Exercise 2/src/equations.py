import numpy as np
from numba import njit


def electric_field(field, h):
    """
    Calculates the magnitude of the electric field at each point on the grid
    """
    return -laplacian(field, h)


def laplacian(field, h):
    height, width = field.shape
    laplacian = np.zeros(field.shape)

    for row in range(height):
        for col in range(width):
            x_component, y_component = (0, 0)

            if row != 0:
                y_component += field[row, col] - field[row - 1, col]
            if row != height - 1:
                y_component += field[row + 1, col] - field[row, col]
            if col != 0:
                x_component += field[row, col] - field[row, col - 1]
            if col != width - 1:
                x_component += field[row, col + 1] - field[row, col]

            laplacian[row, col] = (
                (y_component / (2 * h)) ** 2 + (x_component / (2 * h)) ** 2
            ) ** 0.5

    return laplacian


def CapacitorPoisson(pvalues, a, d, h, N, Q):
    """
    Creates a grid of charge which simulates a capacitor
    """
    caplen = a
    yloc = [-d / 2, d / 2]
    xloc = [0, 0]
    capx1 = np.arange(
        int(N[1] / 2 - caplen / (2 * h) + xloc[0] / h),
        int(N[1] / 2 + caplen / (2 * h) + xloc[0] / h),
    )
    capx2 = np.arange(
        int(N[1] / 2 - caplen / (2 * h) + xloc[1] / h),
        int(N[1] / 2 + caplen / (2 * h) + xloc[1] / h),
    )
    for i in capx1:
        pvalues[int(N[0] / 2 + yloc[0] / h), i] = -Q / 2  # (8.85 * 10 ** (-12))
    for i in capx2:
        pvalues[int(N[0] / 2 + yloc[1] / h) - 1, i] = Q / 2  # (8.85 * 10 ** (-12))
    return pvalues


def CapacitorLaplace(pvalues, fixedV, a, d, h, N, V):
    """
    Creates a grid of potential which simulates a capacitor
    """
    caplen = a
    yloc = [-d / 2, d / 2]
    xloc = [0, 0]
    capx1 = np.arange(
        int(N[1] / 2 - caplen / (2 * h) + xloc[0] / h),
        int(N[1] / 2 + caplen / (2 * h) + xloc[0] / h),
    )
    capx2 = np.arange(
        int(N[1] / 2 - caplen / (2 * h) + xloc[1] / h),
        int(N[1] / 2 + caplen / (2 * h) + xloc[1] / h),
    )
    for i in capx1:
        pvalues[int(N[0] / 2 + yloc[0] / h), i] = (
            -V / 2
        )  # Sets the potential at a point
        fixedV[
            int(N[0] / 2 + yloc[0] / h), i
        ] = 1  # Sets that point as a boundary condition
    for i in capx2:
        pvalues[int(N[0] / 2 + yloc[1] / h), i] = V / 2
        fixedV[int(N[0] / 2 + yloc[1] / h), i] = 1
    return pvalues, fixedV


@njit
def jacobi(field, charge, h):
    """
    Runs the Jacobi method for a grid
    """
    assert field.shape == charge.shape
    new_field = np.zeros_like(field)
    height, width = new_field.shape

    for row in range(height):
        for col in range(width):
            new_field[row, col] = (
                average_surrounding_values(field, row, col) + charge[row, col] * h**2
            )

    return new_field


@njit
def gauss_seidel(field, charge, h):
    """
    Runs the Gauss-Seidel method for a grid
    """
    assert field.shape == charge.shape
    height, width = field.shape
    new_field = field.copy()

    for row in range(height):
        for col in range(width):
            new_field[row, col] = (
                average_surrounding_values(new_field, row, col)
                + charge[row, col] * h**2
            )

    return new_field


@njit
def average_surrounding_values(array, row: int, col: int):
    total = 0
    height, width = array.shape

    if row != 0:
        total += array[row - 1, col]
    if row != height - 1:
        total += array[row + 1, col]
    if col != 0:
        total += array[row, col - 1]
    if col != width - 1:
        total += array[row, col + 1]

    return total / 4

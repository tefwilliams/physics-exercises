import numpy as np
from numba import njit, jit


def get_electric_field(field, h):
    """
    Calculates the magnitude of the electric field at each point on the grid
    """
    return -laplacian(field, h)


@njit
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


def create_capacitor(
    grid_dimensions: tuple[int, int], plate_length: int, plate_separation: int
):
    """
    Creates a grid of charge which simulates a capacitor
    """
    charge_field = np.zeros(grid_dimensions)
    height, width = grid_dimensions

    plates_start_row = (height - plate_length) // 2
    plates_start_col = (width - plate_separation) // 2

    left_plate = (
        range(plates_start_row, plates_start_row + plate_length),
        plates_start_col,
    )
    right_plate = (
        range(plates_start_row, plates_start_row + plate_length),
        plates_start_col + plate_separation,
    )

    charge_field[left_plate] = 100
    charge_field[right_plate] = -100

    return charge_field


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
    count = 0

    height, width = array.shape

    if row != 0:
        total += array[row - 1, col]
        count += 1
    if row != height - 1:
        total += array[row + 1, col]
        count += 1
    if col != 0:
        total += array[row, col - 1]
        count += 1
    if col != width - 1:
        total += array[row, col + 1]
        count += 1

    return total / count

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

from numba import njit

from equations import gauss_seidel, jacobi, get_electric_field, create_capacitor


def is_almost_same(field1, field2):
    return np.all(
        np.divide(
            field1 - field2,
            field2,
            out=np.ones_like(field1),
            where=field2 != 0,
        )
        < 10**-5
    )


def relax_poisson(charge_field, iterative_method):
    """
    Uses finite-difference to 'relax' into a solution to Laplace's or Poisson's equation
    """
    number_of_iterations = 100000
    potential_field_record = [np.zeros(charge_field.shape)]

    for i in range(number_of_iterations):
        old_potential_field = potential_field_record[-1]
        new_potential_field = iterative_method(old_potential_field, charge_field)

        potential_field_record.append(new_potential_field)

        if is_almost_same(new_potential_field, old_potential_field):
            print(f"\nConverged after {i} iterations")
            break

    return potential_field_record


def relax_laplace(potential_field, iterative_method, h):
    """
    Uses finite-difference to 'relax' into a solution to Laplace's or Poisson's equation
    """
    number_of_iterations = 100000
    potential_field_record = [potential_field]

    for i in range(number_of_iterations):
        old_potential_field = potential_field_record[-1]
        new_potential_field = iterative_method(
            old_potential_field, np.zeros_like(potential_field)
        )

        new_potential_field = reset_fixed_potentials(
            potential_field, new_potential_field
        )
        potential_field_record.append(new_potential_field)

        if is_almost_same(new_potential_field, old_potential_field):
            print(f"\nConverged after {i} iterations")
            break

    return potential_field_record


@njit
def reset_fixed_potentials(fixed_potential_field, potential_field):
    updated_field = potential_field.copy()
    height, width = fixed_potential_field.shape

    for row in range(height):
        for col in range(width):
            initial_value = fixed_potential_field[row, col]

            if initial_value != 0:
                updated_field[row, col] = initial_value

    return updated_field


# Sets initial charge field and runs sim

charge_field = create_capacitor((100, 60), 80, 20)

start = time.time()
potential_record = relax_poisson(charge_field, gauss_seidel)
end = time.time()
print(f"\n'relax' took {(end - start):.4g}s to run")

# Plots animation showing sim progression

# fig, (ax1, ax2) = plt.subplots(2)

# electric_field_record = [get_electric_field(field) for field in potential_record]
# ax1.imshow(potential_record[0])
# ax2.imshow(electric_field_record[0])


# def update(frame):
#     ax1.imshow(potential_record[frame])
#     ax2.imshow(electric_field_record[frame])


# ani = animation.FuncAnimation(fig, update, frames=range(0, len(potential_record), 5))
# plt.show()

# Plots a figure of the latest potential

potential_field = potential_record[-1]
e_y, e_x = get_electric_field(potential_field)

fig, ax = plt.subplots()
# ax.plot(potential_field[50])

field_strength = np.linalg.norm([e_y, e_x], axis=0)
# ax.plot(field_strength[50])

# image = ax.imshow(potential_field)

image = ax.imshow(field_strength)
image = ax.quiver(e_x, e_y)


plt.show()

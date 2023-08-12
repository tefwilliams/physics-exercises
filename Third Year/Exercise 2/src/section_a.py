import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

from equations import jacobi, electric_field


def is_almost_same(field1, field2):
    return np.all(
        np.divide(
            field1 - field2,
            field2,
            out=np.ones_like(field1),
            where=field2 != 0,
        )
        < 0.01
    )


def relax(charge_field, iterative_method, h):
    """
    Uses finite-difference to 'relax' into a solution to Laplace's or Poisson's equation
    """
    number_of_iterations = 10000
    potential_field_record = [np.zeros(charge_field.shape)]

    for _ in range(number_of_iterations):
        old_potential_field = potential_field_record[-1]
        new_potential_field = iterative_method(old_potential_field, charge_field, h)

        potential_field_record.append(new_potential_field)

        if is_almost_same(new_potential_field, old_potential_field):
            break

    return potential_field_record


# Sets initial charge field and runs sim

charge_field = np.zeros((100, 60))

plate_length = 80
plate_separation = 20

height, width = charge_field.shape

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

start = time.time()
potential_record = relax(charge_field, jacobi, 0.01)
end = time.time()
print(f"\n'relax' took {(end - start):.4g}s to run")

# Plots animation showing sim progression

# fig, ax = plt.subplots()
# image = ax.imshow(potential_record[0])


# def update(frame):
#     ax.imshow(potential_record[frame])


# ani = animation.FuncAnimation(fig, update, save_count=100)
# plt.show()

# Plots a figure of the latest potential

potential_field = potential_record[-1]
electric_field = electric_field(potential_field, 0.01)

fig, ax = plt.subplots()
image = ax.imshow(potential_field)
# image = ax.imshow(electric_field)
plt.show()

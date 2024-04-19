import numpy as np


gravitational_constant = -9.81
mass = 100

drag_coefficient = 0.6
sea_level_air_density = 1.2
area = 1

atmospheric_scale_factor = 10400


def get_acceleration(velocity: float, air_density: float):
    return gravitational_constant + get_drag(velocity, air_density) / mass


def get_drag(velocity: float, air_density: float):
    return -get_drag_constant(air_density) * abs(velocity) * velocity


def get_drag_constant(air_density: float):
    return 1 / 2 * drag_coefficient * air_density * area


def get_variable_air_density(height: float):
    return sea_level_air_density * np.exp(-height / atmospheric_scale_factor)


def get_fixed_air_density(_: float = 0):
    return sea_level_air_density


# ----------------- ANALYTICAL FUNCTIONS -----------------


def get_analytical_accelerations(time_steps: list[float]):
    # TODO - should this even exist?
    # You don't really get acceleration from Euler, RK etc.
    return [get_analytical_acceleration(time) for time in time_steps]


def get_analytical_acceleration(time: float):
    velocity = get_analytical_velocity(time)
    air_density = get_fixed_air_density()
    return get_acceleration(velocity, air_density)


def get_analytical_velocities(time_steps: list[float]):
    return [get_analytical_velocity(time) for time in time_steps]


def get_analytical_velocity(time: float):
    direction = gravitational_constant / abs(gravitational_constant)
    air_density = get_fixed_air_density()
    drag_constant = get_drag_constant(air_density)
    return (
        direction
        * np.sqrt(mass * abs(gravitational_constant) / drag_constant)
        * np.tanh(np.sqrt(drag_constant * abs(gravitational_constant) / mass) * time)
    )


def get_analytical_heights(initial_height: float, time_steps: list[float]):
    return [get_analytical_height(initial_height, time) for time in time_steps]


def get_analytical_height(initial_height: float, time: float):
    direction = gravitational_constant / abs(gravitational_constant)
    air_density = get_fixed_air_density()
    drag_constant = get_drag_constant(air_density)
    return initial_height + (
        direction
        * (mass / (2 * drag_constant))
        * np.log(
            np.cosh(np.sqrt(drag_constant * abs(gravitational_constant) / mass) * time)
            ** 2
        )
    )

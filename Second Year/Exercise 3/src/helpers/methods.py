from enum import Enum
from typing import Callable, Tuple, TypedDict


Method = Callable[
    [Callable[[float, float], float], Callable[[float], float], float, float, float],
    Tuple[float, float],
]


class MethodString(str, Enum):
    EULER = "euler"
    MODIFIED_EULER = "modified euler"
    RUNGE_KUTTA = "runge kutta"

    def to_method(self) -> Method:
        match self:
            case MethodString.EULER:
                return euler

            case MethodString.MODIFIED_EULER:
                return modified_euler

            case MethodString.RUNGE_KUTTA:
                return runge_kutta

            case _:
                raise ValueError(f"{self} is not a valid method")


IterationData = TypedDict(
    "IterationData",
    {
        "acceleration": list[float],
        "velocity": list[float],
        "height": list[float],
        "time": list[float],
    },
)


def iterate(
    initial_height: float,
    initial_velocity: float,
    acceleration: Callable[[float, float], float],
    air_density: Callable[[float], float],
    method: Method,
    time_step: float,
) -> IterationData:
    acceleration_record = [acceleration(initial_velocity, air_density(initial_height))]
    velocity_record = [initial_velocity]
    height_record = [initial_height]
    time_record = [0.0]

    while height_record[-1] > 0:
        current_velocity = velocity_record[-1]
        current_height = height_record[-1]

        new_velocity, new_height = method(
            acceleration, air_density, current_velocity, current_height, time_step
        )

        acceleration_record.append(
            acceleration(current_velocity, air_density(current_height))
        )
        velocity_record.append(new_velocity)
        height_record.append(new_height)
        time_record.append(time_record[-1] + time_step)

    return {
        "acceleration": acceleration_record,
        "velocity": velocity_record,
        "height": height_record,
        "time": time_record,
    }


def euler(
    acceleration: Callable[[float, float], float],
    air_density: Callable[[float], float],
    current_velocity: float,
    current_height: float,
    time_step: float,
):
    new_velocity = current_velocity + time_step * acceleration(
        current_velocity, air_density(current_height)
    )
    new_height = current_height + time_step * current_velocity

    return new_velocity, new_height


def modified_euler(
    acceleration: Callable[[float, float], float],
    air_density: Callable[[float], float],
    current_velocity: float,
    current_height: float,
    time_step: float,
):
    mid_velocity, mid_height = euler(
        acceleration,
        air_density,
        current_velocity,
        current_height,
        time_step / 2,
    )

    new_velocity = current_velocity + time_step * acceleration(
        mid_velocity, air_density(mid_height)
    )
    new_height = current_height + time_step * mid_velocity

    return new_velocity, new_height


def runge_kutta(
    acceleration: Callable[[float, float], float],
    air_density: Callable[[float], float],
    current_velocity: float,
    current_height: float,
    time_step: float,
):
    δv1 = acceleration(current_velocity, air_density(current_height)) * time_step
    δh1 = current_velocity * time_step

    δv2 = (
        acceleration(current_velocity + δv1 / 2, air_density(current_height + δh1 / 2))
        * time_step
    )
    δh2 = (current_velocity + δv1 / 2) * time_step

    δv3 = (
        acceleration(current_velocity + δv2 / 2, air_density(current_height + δh2 / 2))
        * time_step
    )
    δh3 = (current_velocity + δv2 / 2) * time_step

    δv4 = (
        acceleration(current_velocity + δv3, air_density(current_height + δh3))
        * time_step
    )
    δh4 = (current_velocity + δv3) * time_step

    new_velocity = current_velocity + (1 / 6) * (δv1 + 2 * δv2 + 2 * δv3 + δv4)
    new_height = current_height + (1 / 6) * (δh1 + 2 * δh2 + 2 * δh3 + δh4)

    return new_velocity, new_height

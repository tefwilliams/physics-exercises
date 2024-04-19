from helpers import (
    get_comma_separated_string,
    input_positive_float,
    input_float,
    iterate,
    get_fixed_air_density,
    plot_differences,
    get_acceleration,
    get_analytical_accelerations,
    get_analytical_velocities,
    get_analytical_heights,
    plot_fall,
    MethodString,
)


def run():
    print("\nYou have chosen part (b)")

    initial_height = 10000
    initial_velocity = 0
    time_step = 0.1

    methods = [
        MethodString.EULER,
        MethodString.MODIFIED_EULER,
        MethodString.RUNGE_KUTTA,
    ]

    while True:
        choice = input(
            f"""
Select one of the following options:
'r': To run the {get_comma_separated_string(method.value for method in methods)} methods with the parameters:
    initial height: {initial_height}m
    initial vertical velocity: {initial_velocity}m/s
    time step: {time_step}s
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print(f"\nYou entered the choice: '{choice}'")

        match choice:
            case "r":

                data = {
                    method.value: iterate(
                        initial_height,
                        initial_velocity,
                        get_acceleration,
                        get_fixed_air_density,
                        method.to_method(),
                        time_step,
                    )
                    for method in methods
                }

                time_steps = data[MethodString.EULER]["time"]

                plot_differences(
                    data,
                    {
                        "acceleration": get_analytical_accelerations(time_steps),
                        "velocity": get_analytical_velocities(time_steps),
                        "height": get_analytical_heights(initial_height, time_steps),
                        "time": time_steps,
                    },
                )

            case "m":
                initial_height = input_positive_float(
                    "Enter a value for the initial height: "
                )
                initial_velocity = input_float(
                    "Enter a value for the initial velocity: "
                )
                time_step = input_positive_float("Enter a value for the time step: ")

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")

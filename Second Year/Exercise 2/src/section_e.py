import numpy as np

from input_helpers import input_float, input_positive_int
from integration import simpson_integrate


def run():
    print("\n" + "You have chosen part (e)")

    # Width of square slit
    slit_width = 0.25 * 10**-3
    wavelength = 600 * 10**-9

    # Coordinates in 3D space
    # from centre of slit
    x = -0.08 * 10**-3
    y = -0.08 * 10**-3
    z = 0.5 * 10**-2

    number_of_steps = 1000

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
'r': To run the section with the following parameters:
    slit width: {slit_width * 10**3:.3g}mm
    wavelength: {wavelength * 10**9:.3g}nm
    x coordinate: {x * 10**3:.3g}mm
    y coordinate: {y * 10**3:.3g}mm
    z coordinate: {z * 10**3:.3g}mm
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "r":
                wavenumber = 2 * np.pi / wavelength

                fresnel = lambda x: lambda xp: np.exp(
                    (1j * wavenumber) / (2 * z) * (x - xp) ** 2
                )

                xp_min = yp_min = -slit_width / 2
                xp_max = yp_max = slit_width / 2

                x_val = simpson_integrate(fresnel(x), xp_min, xp_max, number_of_steps)
                y_val = simpson_integrate(fresnel(y), yp_min, yp_max, number_of_steps)

                constant = wavenumber / (2 * np.pi * z)
                intensity = abs(constant * x_val * y_val)

                print("\n" + f"The value of the Fresnel integral is: {intensity:.3g}")

            case "m":
                slit_width = (
                    input_float("Enter a value for the slit width (in mm): ") * 10**-3
                )
                wavelength = (
                    input_float("Enter a value for the wavelength (in nm): ") * 10**-9
                )
                x = (
                    input_float("Enter a value for the x coordinate (in mm): ")
                    * 10**-3
                )
                y = (
                    input_float("Enter a value for the y coordinate (in mm): ")
                    * 10**-3
                )
                z = (
                    input_float("Enter a value for the z coordinate (in mm): ")
                    * 10**-3
                )
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")

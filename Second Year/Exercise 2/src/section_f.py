import numpy as np
from matplotlib import pyplot as plt

from input_helpers import input_float, input_positive_int
from integration import simpson_integrate


def run():
    print("\n" + "You have chosen part (f)")

    # Width of square slit
    slit_width = 0.25 * 10**-3
    # Width of image square
    image_width = 0.4 * 10**-3
    wavelength = 600 * 10**-9

    z = 0.5 * 10**-2

    number_of_steps = 1000
    number_of_points = 1000

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
'r': To run the section with the following parameters:
    slit width: {slit_width * 10**3:.3g}mm
    image size: {image_width * 10**3:.3g}mm
    wavelength: {wavelength * 10**9:.3g}nm
    z coordinate: {z * 10**3:.3g}mm
    number of points: {number_of_points}
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "r":
                wavenumber = 2 * np.pi / wavelength
                fresnel = np.vectorize(
                    lambda x: lambda xp: np.exp(
                        (1j * wavenumber) / (2 * z) * (x - xp) ** 2
                    )
                )

                x_min = y_min = -image_width / 2
                x_max = y_max = image_width / 2

                x = np.linspace(x_min, x_max, number_of_points)
                y = np.linspace(y_min, y_max, number_of_points)

                xp_min = yp_min = -slit_width / 2
                xp_max = yp_max = slit_width / 2

                x_vals = np.vectorize(simpson_integrate)(
                    fresnel(x), xp_min, xp_max, number_of_steps
                )
                y_vals = np.vectorize(simpson_integrate)(
                    fresnel(y), yp_min, yp_max, number_of_steps
                )

                constant = wavenumber / (2 * np.pi * z)
                intensity = abs(constant * np.outer(x_vals, y_vals))

                plt.imshow(
                    intensity,
                    extent=[x_min * 1000, x_max * 1000, y_min * 1000, y_max * 1000],
                    cmap="jet",
                )
                plt.title("Intensity")
                plt.locator_params(axis="y", nbins=5)
                plt.locator_params(axis="x", nbins=5)
                plt.figtext(1, 0.7, f"z: {z * 10**3:.3g}mm")
                plt.figtext(1, 0.6, f"wavenumber: {wavenumber:.3}radm^{-1}")
                plt.figtext(1, 0.5, f"slit width: {slit_width}mm")
                plt.figtext(
                    1,
                    0.3,
                    f"Number of points in x and y directions: {number_of_points}",
                )
                plt.xlabel("$x$ $(mm)$")
                plt.ylabel("$y$ $(mm)$")
                plt.show()

            case "m":
                slit_width = (
                    input_float("Enter a value for the slit width (in mm): ") * 10**-3
                )
                image_width = (
                    input_float("Enter a value for the image width (in mm): ")
                    * 10**-3
                )
                wavelength = (
                    input_float("Enter a value for the wavelength (in nm): ") * 10**-9
                )
                z = (
                    input_float("Enter a value for the z coordinate (in mm): ")
                    * 10**-3
                )
                number_of_points = input_positive_int(
                    "Enter a value for the number of steps: "
                )
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")

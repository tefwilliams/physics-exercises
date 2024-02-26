from input_helpers import input_float, input_positive_int
from integration import simpson_integrate
from input_helpers import get_1d_function


def run():
    print("\n" + "You have chosen part (a)")

    lower_bound = 0
    upper_bound = 1
    number_of_steps = 100

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
Enter a function to be intergrated with the following parameters:
    lower bound: {lower_bound}
    upper bound: {upper_bound}
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "m":
                lower_bound = input_float("Enter a value for the lower bound: ")
                upper_bound = input_float("Enter a value for the upper bound: ")
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )
            case "q":
                break
            case _:
                try:
                    integral_value = simpson_integrate(
                        get_1d_function(choice),
                        lower_bound,
                        upper_bound,
                        number_of_steps,
                    )

                    print(
                        "\n"
                        + f"The integral of {choice} between {lower_bound} and {upper_bound} is: {integral_value:.3g}"
                    )

                except ValueError as e:
                    print(e)

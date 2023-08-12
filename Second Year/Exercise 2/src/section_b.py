from input_helpers import input_float, input_positive_int
from integration import simpson_integrate
from repository import mysin, mycos


def run():
    print("\n" + "You have chosen part (b)")

    lower_bound = 0
    upper_bound = 1
    number_of_steps = 100

    while True:
        choice = input(
            "\n"
            + f"""Select one of the following options:
'sine' or 'cosine': To integrate the relevant Fresnel function with the following parameters:
    lower bound: {lower_bound}
    upper bound: {upper_bound}
    number of steps: {number_of_steps}
'm': To modify the parameters
'q': To return to the previous menu

"""
        )

        print("\n" + f"You entered the choice: '{choice}'")

        match choice:
            case "sine" | "cosine":
                try:
                    # Evaluates S(w) or C(w) as asked
                    function = mysin if choice == "sine" else mycos

                    integral_value = simpson_integrate(
                        function, lower_bound, upper_bound, number_of_steps
                    )

                    print(
                        "\n"
                        + f"The integral of the {choice} function between {lower_bound} and {upper_bound} is: {integral_value:.3g}"
                    )

                except ValueError as e:
                    print(e)

            case "m":
                lower_bound = input_float("Enter a value for the lower bound: ")
                upper_bound = input_float("Enter a value for the upper bound: ")
                number_of_steps = input_positive_int(
                    "Enter a value for the number of steps: "
                )

            case "q":
                break

            case _:
                print("\n" + "This is not a valid choice")

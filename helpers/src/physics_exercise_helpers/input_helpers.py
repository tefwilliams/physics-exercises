from .module_helpers import get_from_module


def input_positive_int(input_string: str):
    while True:
        choice = input_int(input_string)

        if choice >= 1:
            return choice

        print(f"{choice} is less than 1")


def input_int(input_string: str):
    while True:
        choice = input(input_string)

        try:
            return int(choice)

        except ValueError:
            print(f"{choice} is not a valid integer")


def input_positive_float(input_string: str):
    while True:
        choice = input_float(input_string)

        if choice > 0:
            return choice

        print(f"{choice} is less than or equal to 0")


def input_float(input_string: str):
    while True:
        choice = input(input_string)

        try:
            return float(choice)

        except ValueError:
            try:
                module_item = get_from_module(choice)

                try:
                    return float(module_item)

                except:
                    print(f"{choice} is not a valid number")

            except Exception as e:
                print(e)

from sections import run_section_a

while True:
    choice = input(
        "\n"
        + """Select one of the following options:
'a': To simulate an electric field using finite difference methods
'b': To simulate a heat distribution using finite difference methods
'q': To quit

"""
    )

    match choice:
        case "a":
            run_section_a()
        # case "b":
        #     run_section_b()
        # case "c":
        #     run_section_c()
        # case "d":
        #     run_section_d()
        # case "e":
        #     run_section_e()
        # case "f":
        #     run_section_f()
        case "q":
            print("\n" + "You have chosen to finish - goodbye.")
            break
        case _:
            print("\n" + "This is not a valid choice")

from sections import (
    run_section_a,
    run_section_b,
    # run_section_c,
    run_section_d,
    run_section_e,
    # run_section_f,
)

while True:
    choice = input(
        "\n"
        + """Select one of the following options:
'a': To simulate a fall with fixed drag
'b': To test the convergence over time with fixed drag
'c': To test the convergence for changing dt with fixed drag
'd': To simulate a fall with varying drag
'e': To test the convergence over time with varying drag
'f': To test the convergence for changing dt with varying drag
'q': To quit

"""
    )

    match choice:
        case "a":
            run_section_a()
        case "b":
            run_section_b()
        # case "c":
        #     run_section_c()
        case "d":
            run_section_d()
        case "e":
            run_section_e()
        # case "f":
        #     run_section_f()
        case "q":
            print("\n" + "You have chosen to finish - goodbye.")
            break
        case _:
            print("\n" + "This is not a valid choice")

from sections import (
    run_section_a,
    run_section_b,
    run_section_c,
    run_section_d,
    run_section_e,
    run_section_f,
)

while True:
    choice = input(
        "\n"
        + """Select one of the following options:
'a': To integrate a chosen function
'b': To evaluate the terms in the Fresnel integrals
'c': To plot I(w)
'd': To test the convergence of the 1D Simpson's rule
'e': To integrate the Fresnel integral
'f': To calculate the diffraction intensity for a grid of (x,y) values and plot these as an image
'q': To quit

"""
    )

    match choice:
        case "a":
            run_section_a()
        case "b":
            run_section_b()
        case "c":
            run_section_c()
        case "d":
            run_section_d()
        case "e":
            run_section_e()
        case "f":
            run_section_f()
        case "q":
            print("\n" + "You have chosen to finish - goodbye.")
            break
        case _:
            print("\n" + "This is not a valid choice")

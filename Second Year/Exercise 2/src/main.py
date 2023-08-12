import section_a
import section_b
import section_c
import section_d
import section_e
import section_f

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
            section_a.run()
        case "b":
            section_b.run()
        case "c":
            section_c.run()
        case "d":
            section_d.run()
        case "e":
            section_e.run()
        case "f":
            section_f.run()
        case "q":
            print("\n" + "You have chosen to finish - goodbye.")
            break
        case _:
            print("\n" + "This is not a valid choice")

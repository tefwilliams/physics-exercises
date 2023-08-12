#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:19:20 2017

@author: thomaswilliams
"""

# Please run in IPython

# Functions

from typing import Callable, Union
from repository import InputStrings, select_section_menu, section_a_menu, section_b_menu

import numpy as np
import matplotlib.pyplot as plt
import time
import sys


def mysin(x: float) -> float:
    'The sine function for the Fresnel integral'
    return np.sin((np.pi * (x ** 2)) / 2)
    

def mycos(x: float) -> float:
    'The cosine function for the Fresnel integral'
    return np.cos((np.pi * (x ** 2)) / 2)

    
def validate_inputs(input_string: str) -> Union[int, float]:
    
    # This function takes the allows each input to be checked for errors without having to write the code multiple times
    
    while True:
        input_value = input(input_string)

        try:
            if input_string in [InputStrings.N, InputStrings.w, InputStrings.xy]:
                input_value = convert_to_int(input_value)
                
                if input_string == InputStrings.N:
                    if input_value <= 0:
                        raise ValueError("You must input a number greater than zero")

                    if is_odd(input_value):
                        raise ValueError("You must input an even number")

                else:
                    if input_value < 2:
                        raise ValueError("You must input a number greater than 1")

            else:
                input_value = convert_to_float(input_value)

                if input_string == InputStrings.wavelength and input_value <= 0:
                    raise ValueError("You must input a number greater than zero")

            return input_value

        except ValueError as e:
            print("\n" + "%s" %e)
                
                
    # These functions process and assign the inputs for each section
                
def get_bounds(section):
    if(section == "b"):
        lower_bound = 0
        value = "Input a value for w: "
        upper_bound = validate_inputs(value)
        return lower_bound, upper_bound

    value = "Input a lower bound: "
    lower_bound = validate_inputs(value)
    value = "Input an upper bound: "
    upper_bound = validate_inputs(value)
    return [lower_bound,upper_bound]

    # For each input, the Input_Test function is run

def Two_D_Inputs(x,y,z,k,p):
    if(section != "f"):
        value = "Input a value for x: "
        x = validate_inputs(value)
        value = "Input a value for y: "
        y = validate_inputs(value)
        value = "Input a value for z: "
        z = validate_inputs(value)
        value = "Input a value for k: "
        k = validate_inputs(value)
        value = "Input a value for p: "
        p = validate_inputs(value)
    elif(section == "f"):
        value = "Input a value for z in centimeters: "
        z = validate_inputs(value) * 10**(-2)
        value = "Input a wavelength in micrometers: "
        wavelength = validate_inputs(value) * 10**(-6)
        k = 2 * pi / wavelength
        value = "Input a value for p in millimeters: "
        p = validate_inputs(value) * 10**(-3)           
    return [x,y,z,k,p]

    # Different strings are used for different sections, to make the program more user friendly
    
def get_number_of_steps() -> int:
    return validate_inputs(InputStrings.N)  
            
def NumPoints_Input(NumPoints):
    if(section == "c"):
        value = "Input a value for the number of points for w: "
    elif(section == "f"):
        value = "Input a value for the number of points in the x and y directions: "
    return validate_inputs(value)
             
    # This is the orginial Simpson's rule function
    
def integrate(function: Callable[[float], float], lower_bound: float, upper_bound: float, number_of_steps: int):    
    sum = 0
    step_size = (upper_bound - lower_bound) / number_of_steps

    for i in range(number_of_steps + 1):
        x = lower_bound + step_size * i

        if i == 0 or i == number_of_steps:
            sum += function(x)

        elif is_odd(i):
            sum += 4 * function(x)

        else:
            sum += 2 * function(x)

    return (step_size / 3) * sum
       
def x_Integral(x,y,z,xp,yp,h,k,p,N):
    
    # The integral with respect to x for the 2-D Simpson's rule
    
    xtotal = 0
    fx = 0        
    for n in range(N + 1) :
        
        # Originally used exp(), but found this too twice as long to run as e**()
        
        function = (k / (2 * pi * z)) * np.e ** ((1j * k) / (2 * z) * ((x - xp) ** 2 + (y - yp) ** 2))
        xp = (-p / 2) + h * n
        if(n == 0 or n == N):
            fx = function
        elif(n%2 != 0):
            fx = 4 * function
        elif(n%2 == 0):
            fx = 2 * function
        xtotal += fx 
    return (h / 3) * xtotal
        
def Two_D_Simpson(x,y,z,k,p,N):
    
    # The integral with respect to y for the 2-D Simpson's rule
    
    xp = 0
    yp = 0   
    h = p / N                    
    ytotal = 0
    fy = 0        
    for n in range(N + 1):
        yp = (-p / 2) + h * n
        if(n == 0 or n == N):
            fy = x_Integral(x,y,z,xp,yp,h,k,p,N)         
        elif(n%2 != 0):
            fy = 4 * x_Integral(x,y,z,xp,yp,h,k,p,N)
        elif(n%2 == 0):
            fy = 2 * x_Integral(x,y,z,xp,yp,h,k,p,N)       
        ytotal += fy                        
    output = (h / 3) * (ytotal)
    
    if(section == "e"):
        print(" ")
        print("The value of the Fresnel integral for the above inputs is:",output)
    else:
        return(output)




# Loop Until Quit
      
def run():
    sections = ["a", "b", "c", "d", "e", "f"]

    while True:
        
        # Resets the variables so they can't accidentally be inputted into functions and defines pi as 'pi' for easier use
        # Allows the user to select section by inputting the section letter
        
        [lower_bound,upper_bound,x,y,z,k,p,number_of_steps,xp,yp,NumPoints] = [None] * 11 

        selected_section = input(select_section_menu)

        if selected_section == "q":
            print("\n" + "You have chosen to finish - goodbye.")
            break

        elif selected_section not in sections:
            print("\n" + "This is not a valid choice")
            continue

        print("\n" + "You have chosen part: (%s)" %selected_section)
        
        # Section A    

        if selected_section == "a":          
            while True:
                entered_input = input(section_a_menu)
                print("\n" + "You entered the choice: %s" %entered_input)
                
                if entered_input == "r":
                    break

                function = validate_input(entered_input)

                if not function:
                    continue
                                        
                # Calls input function and the required variables from the list generated by this function

                lower_bound, upper_bound = get_bounds(selected_section)
                number_of_steps = get_number_of_steps()

                integral_value = integrate(function, lower_bound, upper_bound, number_of_steps)
                print("The integral of %s for the above inputs is: %.3g" %(entered_input, integral_value))

            
        # Section B
            
        elif selected_section == "b":
            while True:
                entered_input = input(section_a_menu)
                print("\n" + "You entered the choice: %s" %entered_input)

                if entered_input == "r":
                    break
                
                # Evaluates S(w) or C(w) as asked
                
                if entered_input == "sine" or entered_input == "cosine":
                    
                    lower_bound, upper_bound = get_bounds(selected_section)
                    number_of_steps = get_number_of_steps()
                        
                    function = mysin if entered_input == "sine" else mycos

                    integral_value = integrate(function, lower_bound, upper_bound, number_of_steps)
                    print("The integral of the", entered_input, "function between 0 and w is:", integral_value)
                        
                else:
                    print("\n" + "This is not a valid choice")
                
        # Section C
            
        elif selected_section == "c":
            print(" ")
            print("You have chosen part (c)")
            
            number_of_steps = get_number_of_steps(number_of_steps)
            NumPoints = NumPoints_Input(NumPoints)
            
            # Takes inputs and as default runs from -5 to 10
            
            wmin = -5
            wmax = 10
            dw = (wmax - wmin) / (NumPoints - 1)
            
            xvals = [0.0] * NumPoints
            yvals = np.zeros(NumPoints)
            
            # Contains timer which allows for countdown to end as well as timing the whole function
            
            print(" ") 
            start = time.time()
            
            for i in range(NumPoints):
                xvals[i] = wmin + i * dw
                yvals[i] = (((integrate(mysin,0,xvals[i],number_of_steps) + 0.5) ** 2 + (integrate(mycos,0,xvals[i],number_of_steps) + 0.5) ** 2) / 2)
                
                # Code for countdown
                
                test = time.time()
                total_time = (test - start) / ((i + 1) / NumPoints)
                time_remaining = total_time - (test - start)
                sys.stdout.write("\r")
                sys.stdout.write("Approximately %.0f seconds remaining.." % time_remaining)
                sys.stdout.flush()
                
            print(" ")                   
            end = time.time()
                
            # Creates plot with x-limits defined as wmin to wmax and labels axes
            
            plt.plot(xvals,yvals)
            plt.title("Intensity at P")
            plt.xlim([wmin,wmax])
            plt.locator_params(axis='y',nbins=5)
            plt.locator_params(axis='x',nbins=5)
            plt.xlabel("$w$")
            plt.ylabel("$I(w)/I_0$")
            plt.show()

            # Shows time for whole function to run
            
            print("The calculation took %.2f seconds." % (end - start))
            
    # Simpson's rule convergence

        elif selected_section == "d":
            print(" ")
            print("You have chosen part (d)")
            
            
            section_selection = "0"
            
            while section_selection != "r":
                section_selection = input("Enter a function for which the convergence of Simpson's rule will be tested; otherwise enter 'r' to return to the previous menu: ")
                print(" ")
                print("You entered the choice:",section_selection)
                
                if section_selection == "r":
                    continue
                
                while True:
                    try:                   
                        try:
                            callback_function = eval(section_selection) 
                                            
                            if(section_selection == "x"):
                                def callback_function(x):
                                    return eval(section_selection)
                                    
                            elif(eval(section_selection) ==  None):
                                print(" ")
                                print("This is not a valid choice")
                                break
                            
                        except(TypeError):             
                            def callback_function(x):
                                return eval(section_selection)
    
                        lower_bound, upper_bound = get_bounds(lower_bound,upper_bound)
                        lower_bound = lower_bound, upper_bound[0]
                        upper_bound = lower_bound, upper_bound[1]
                        number_of_steps = get_number_of_steps(number_of_steps)
                        xvals = [0.0] * number_of_steps
                        yvals = [0.0] * number_of_steps
                        actual_xvals = [0.0] * number_of_steps
                        actual_value = [0.0] * number_of_steps
    
                        print(" ")
                        start = time.time()
                        value = integrate(callback_function,lower_bound,upper_bound,100000)
                    
                        # Creates array for 'true' value of integral
                        
                        for i in range(number_of_steps+1):
                            actual_xvals.append(i)
                            actual_value.append(value)
                            
                        # Increases N for the function with given xmin and xmax    
                        
                        for i in range(2,number_of_steps+1,2):
                            xvals.append(i)
                            yvals.append(integrate(callback_function,lower_bound,upper_bound,i))
                            
                            test = time.time()
                            total_time = (test - start) / ((i + 1) / (number_of_steps+1))
                            time_remaining = total_time - (test - start)
                            sys.stdout.write("\r")
                            sys.stdout.write("Approximately %.0f seconds remaining.." % time_remaining)
                            sys.stdout.flush()                    
                        
                        print(" ")                   
                        end = time.time()
                
                        # Creates a plot and also plots on the 'true' value of the integral (found using N of 100000)
                
                        plt.plot(xvals,yvals)
                        plt.plot(actual_xvals,actual_value)
                        plt.title("Convergence of the 1-D Simpson rule")
                        plt.xlim([0,number_of_steps])
                        plt.locator_params(axis='y',nbins=5)
                        plt.locator_params(axis='x',nbins=5)
                        plt.xlabel("$N$")
                        plt.ylabel("Integral of $f(x)$")
                        plt.show()
            
                        print("The calculation took %.2f seconds." % (end - start))  
                        break
                    
                    # Keeps spacing the same in console
                    
                    except Exception:
                        if section_selection != "r":
                            if TypeError:
                                print("This is not a valid choice")
                            else:
                                print(" ")
                                print("This is not a valid choice")
                        break
                continue
        
    # Section E
            
        elif selected_section == "e":
            print(" ")
            print("You have chosen part (e)")
            
            # Takes inputs using input function as before and runs 2-D Simpson's rule function from those inputs
            
            lower_bound, upper_bound = Two_D_Inputs(x,y,z,k,p)
            x = lower_bound, upper_bound[0]
            y = lower_bound, upper_bound[1]
            z = lower_bound, upper_bound[2]
            k = lower_bound, upper_bound[3]
            p = lower_bound, upper_bound[4]
            number_of_steps = get_number_of_steps(number_of_steps)
            
            Two_D_Simpson(x,y,z,k,p,number_of_steps)
            
    # Section F
            
        elif selected_section == "f":
            print(" ")
            print("You have chosen part (f)")

            lower_bound, upper_bound = Two_D_Inputs(x,y,z,k,p)
            z = lower_bound, upper_bound[2]
            k = lower_bound, upper_bound[3]
            p = lower_bound, upper_bound[4]
            number_of_steps = get_number_of_steps(number_of_steps)
            NumPoints = NumPoints_Input(NumPoints)
            
            # x and y limits defined separately to make them easier to change
            
            lower_bound = -0.2 * 10**(-3)
            upper_bound = 0.2 * 10**(-3)
            ymin = -0.2 * 10**(-3)
            ymax = 0.2 * 10**(-3)         
            dx = (upper_bound - lower_bound) / (NumPoints - 1)  
            dy = (ymax - ymin) / (NumPoints - 1)
            intensity = np.zeros((NumPoints,NumPoints))
            
            # The same timer code as before is used - not worth writing a funtion due to few lines of code and where the code is positioned
            
            print(" ")
            start = time.time()
            
            # Runs nested loops so that every i,j combination is reached for the 2-D array and records modulus squared value of the function for each point
            
            for i in range(NumPoints):
                x = lower_bound + i * dx
                
                for j in range(NumPoints):
                    y = ymin + j * dy
                    intensity[i,j] = abs(Two_D_Simpson(x,y,z,k,p,number_of_steps)) ** 2

                test = time.time()
                total_time = (test - start) / ((i + 1) / NumPoints)
                time_remaining = total_time - (test - start)
                sys.stdout.write("\r")
                sys.stdout.write("Approximately %.0f seconds remaining.." % time_remaining)
                sys.stdout.flush()
    
            print(" ")                   
            end = time.time()
            
            # Plots array with limits given by the limits of x and y
            # Also gives the values of the inputs to the side of the plot
            # Fixes the number of values on x and y axes due to there being too many by default
            # Plots colourbar and labels axes
                    
            plt.imshow(intensity, extent=[lower_bound*1000,upper_bound*1000,ymin*1000,ymax*1000])
            plt.title("Intensity")
            plt.locator_params(axis='y',nbins=5)
            plt.locator_params(axis='x',nbins=5)
            plt.figtext(1,0.7," z: "+str(z * 100)+" $cm$")
            plt.figtext(1,0.6,"k: "+str(round(k))+" $radm^{-1}$")
            plt.figtext(1,0.5,"p: "+str(p * 1000)+" $mm$")
            plt.figtext(1,0.4,"N: "+str(number_of_steps))
            plt.figtext(1,0.3,"Number of points in (x,y) directions: "+str(NumPoints))
            plt.xlabel("$x$ $(mm)$")
            plt.ylabel("$y$ $(mm)$")
            plt.colorbar()
            plt.show()
            
            print("The calculation took %.2f seconds." % (end - start))
                            
        elif selected_section ==  "q":
                print(" ")
                print("You have chosen to finish - goodbye.")

        
        else:
            print(" ")
            print("This is not a valid choice")
            
    selected_section="0" 

run()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:36:51 2018

@author: thomaswilliams
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import stats
import imageio
import time
import os
import sys
import csv

# -------------- PARAMETER SETTING -------------- 

def InputTest(name, value, conditions):
    '''
    Checks inputs for validity
    '''
    while True:
        try:
            parameter = input(value) # Prints a description of the input value
            if name in ['Gauss', 'Gif', 'CSV', 'Singlegraph', 'Multigraph']:
                if parameter in ['True', 'False']:
                    return eval(parameter) # Optional settings - return 'True' or 'False'
                else:
                    print("You must enter 'True' or 'False'. \n")
                    continue
            if name in ['xlen', 'ylen', 'h', 't', 'dt', 'k', 'c', 'p', 'a', 'd', 'criterion'] and float(parameter) < 0:
                print('\n' + 'You must enter a positive number.')
                continue
            if name in ['iterations']:
                if int(parameter) != float(parameter) or int(parameter) < 1:
                    print('\n' + 'You must enter an interger greater than one.')
                    continue
                else:
                    return int(parameter)
            if name in ['h', 'a'] and float(parameter) > min(conditions): # Allows previous values to be compared to
                print('\n' + 'You must enter a number no larger than the grid dimensions.')
                continue
            if name in ['d'] and float(parameter) >= min(conditions):
                print('\n' + 'You must enter a number smaller than the grid dimensions.')
                continue
            if name in ['dt'] and float(parameter) > conditions:
                print('\n' + 'You must enter a number smaller than the run time.')
                continue
            return float(parameter)
        except Exception:
            print('\n' + 'This is not a valid input.')

def ParamSet(params, sections, task, inputselection):
    '''
    Allows the setting of parameters
    '''
    if task == 'Initial': # Initialises parameters and optional settings
        sections = ['On', False, False, False, True, True]
        task1params = [3000, 20, 2000, 2, 1, 0.05, 1, 0.2, 0]
        task2params = [30000, 1, 59, 450, 7900, 0.5, 0.02, 0.01, 0.001]
        return [sections, task1params, task2params]

    elif task == 'Exercise 1': # Allows user enable/disable optional settings - passes inputs through input tester
        [Menu, Gauss, Gif, CSV, Singlegraph, Multigraph] = sections
        print('\n' + "Enter 'True' to enable, or 'False' to disable, the options. \n")
        Gauss = InputTest('Gauss', 'Gauss-Seidel Method: ', None)
        Gif = InputTest('Gif', 'Gif: ', None)
        CSV = InputTest('CSV', 'CSV: ', None)
        Singlegraph = InputTest('Singlegraph', 'Singlegraph: ', None)
        Multigraph = InputTest('Multigraph', 'Multigraph: ', None)
        return [Menu, Gauss, Gif, CSV, Singlegraph, Multigraph]
    
    elif task == 'Task 1': # Allows user to change values (task 1) - passes inputs through input tester
        [iterations, Q, V, xlen, ylen, h, a, d, criterion] = params
        iterations = InputTest('iterations', 'Input a value for the number of iterations: ', None)
        if inputselection == 'a':
            Q = InputTest('Q', 'Input value for the magnitude of charge density on the plates (C/m^3): ', None)
            V = InputTest('V', 'Input a value for the voltage across the plates (V): ', None)
            xlen = InputTest('xlen', 'Input a value for the x-dimension of the grid (m): ', None)
            ylen = InputTest('ylen', 'Input a value for the y-dimension of the grid (m): ', None)
            a = InputTest('a', 'Input a value for the length of the capacitor plates (m): ', [xlen])
            d = InputTest('d', 'Input a value for distance between the plates (m): ', [ylen])
        h = InputTest('h', 'Input a value for the point separation (m): ', [xlen / 2, ylen / 2])
        criterion = InputTest('criterion', 'Input a value for the convergence criterion (%): ', None)
        return [iterations, Q, V, xlen, ylen, h, a, d, criterion]
    
    elif task == 'Task 2': # Allows user to change values (task 2) - passes inputs through input tester
        [t, dt, k, c, p, xlen, ylen, h, criterion] = params
        t = InputTest('t', 'Input a value for the run time (s): ', None)
        dt = InputTest('dt', 'Input a value for the time-step (s): ', t)
        k = InputTest('k', 'Input a value for k (W/m/K): ', None)
        c = InputTest('c', 'Input a value for c (J/kg/K): ', None)
        p = InputTest('p', 'Input a value for p (kg/m^3): ', None)
        if inputselection == 'a':
            xlen = InputTest('xlen', 'Input a value for the x-dimension of the grid (m): ', None)
            ylen = InputTest('ylen', 'Input a value for the y-dimension of the grid (m): ', None)
        h = InputTest('h', 'Input a value for the point separation (m): ', [xlen / 2, ylen / 2])
        criterion = InputTest('criterion', 'Input a value for the convergence criterion (%): ', None)
        return [t, dt, k, c, p, xlen, ylen, h, criterion]
 
# -------------- MENU SYSTEM -------------- 

def Exercise2(variables): # Base structure from which the whole code is run
    '''
    Provides a menu system to sort between the different tasks
    '''
    [sections, task1params, task2params] = variables # Calls initialised parameters
    [Menu, Gauss, Gif, CSV, Singlegraph, Multigraph] = sections # Calls initialised optional settings
    print('\n' + '''The 'Optional Sections' have been set as the following: \n
    Gauss-Seidel Method: %s
    GIF: %s
    CSV: %s
    Singlegraph: %s
    Multigraph: %s ''' %(Gauss, Gif, CSV, Singlegraph, Multigraph)) # Prints the status of optional settings
    
    taskselection = input('''Enter a choice: \n
    'a' (To run the Laplace Function),
    'b' (To run the Poisson Function),
    'c' (To run the Diffusion Function),
    'd' (To enable / disable the 'Optional Sections')
    'q' (To quit): ''') # Allows the user to choose the section to run from within the console
    print('\n' + 'You entered the choice: %s \n' % taskselection)
    
    if taskselection == 'q':
        print('You have chosen to finish - goodbye. \n')
        return 'q', sections
    
    elif taskselection not in ['a', 'b', 'c', 'd']: # Checks validity of input
        print('\n' + 'This is not a valid choice. \n')
    
    elif taskselection == 'a': # Runs different sections depending on the user input
        task1selection = 0
        while task1selection != 'r': # Runs the relaxation section for Laplace
            task1selection = Task1(task1params, sections, False)
            
    elif taskselection == 'b':
        task1selection = 0
        while task1selection != 'r': # Runs the relaxation section for Poisson
            task1selection = Task1(task1params, sections, True)
            
    elif taskselection == 'c':
        task2selection = 0
        while task2selection != 'r': # Runs the diffusion section
            task2selection = Task2(task2params, sections)
            
    elif taskselection == 'd': # Allows the user to enable/disable optional settings
        sections = ParamSet(None, sections, 'Exercise 1', None)
        
    return None, sections

# -------------- SHARED FUNCTIONS -------------- 

def FileWrite(file_name, variables): # Function to write data to a .csv file
    '''
    Writes specified information to a .csv file
    '''
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(variables)
        
def Directory(folder_name): # Function to find the path to a named folder (or create a names folder if it doesn't exist)
    '''
    Finds the path to a named folder or creates folder with specified name
    '''
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    script_dir = os.path.dirname(__file__)
    results_dir = script_dir + '/' + folder_name + '/'
    return results_dir
    
def Convergence(pold, pnew, N, n, iterations, criterion): # Convergence tester
    '''
    Tests two arrays and returns 'True' if either the convergence condition or maximum number of iterations has been reached
    '''
    converg = criterion / 100
    if np.allclose(pold, pnew, rtol = converg, atol = 0):
        print('\n' + 'The loop converged after %s iterations.' %(n))
        return True
    elif n >= iterations - 2:
        print('\n' + 'The loop was broken as the maximum number of iterations was hit.')
        return True
    else:
        return False
    
def CSVImport(testarray): # Allows the user to import arrays for the different tasks
    '''
    Imports the data from a .csv file
    '''
    while True:
        c = 0
        try:
            file_name = input('Input the name of the .csv file you wish to import: ')
            array = np.genfromtxt('%s' %(file_name), delimiter=',')
            if testarray is not None:
                if testarray.shape != array.shape: # Checks that a boundary condition array has the same dimensions as the main array
                    print('\n' + 'The boundary conditions file must have the same dimensions as the distribution file.')
                    continue
                for i in array.flatten():
                    if i != 0 and i != 1:
                        c = 1
            if c == 1: # Checks that the boundary condition array has valid inputs
                print('\n' + "All values must be '1' or '0'.")
                continue
            return array
        except: # Prevents crash if file cannot be found
            print('\n' + 'Please check the the .csv file is in the same folder as the python code.')
            print('\n' + 'Also check that the entered name matches that of the file, including any extensions.')
    
# -------------- RELAXATION MENU --------------     

def Task1(params, sections, Poisson): # Base structure for task 1
    '''
    Provides a menu system for Task 1 (the relaxation section)
    '''
    [iterations, Q, V, xlen, ylen, h, a, d, criterion] = params # Sets values of parameters and options
    [Menu, Gauss, Gif, CSV, Singlegraph, Multigraph] = sections
    inputselection = 'a' 
    
    if Menu == 'On':  
        inputselection = input('''Enter a choice: \n
        'a' (To simulate a Capacitor),
        'b' (To input a different array): ''') # Allows the user to choose the section to run from within the console
        print('\n' + 'You entered the choice: %s \n' % inputselection) 
        
        if inputselection not in ['a', 'b']: # Checks validity of input
            print('\n' + 'This is not a valid choice. \n')
            return
        
        elif Poisson and inputselection == 'b': # Prompts user to create and import .csv file
            print('\n' + 'Please create a .csv file with the sought after charge distribution.')
            charge = CSVImport(None)
            Nx, Ny = charge.shape[1], charge.shape[0] # From .csv file generates required arrays
            potential0, setvalues = np.zeros(charge.shape), np.zeros(charge.shape)
                 
        elif not Poisson and inputselection == 'b': # Prompts user to create and import .csv file
            print('\n' + 'Please create a .csv file with the sought after potential distribution.')
            potential0 = CSVImport(None)
            Nx, Ny = potential0.shape[1], potential0.shape[0]
            print('\n' + "Please create a .csv file for the boundary conditions. Place '1' at any points to remain unchanged and '0' elsewhere.")
            setvalues = CSVImport(potential0) # From .csv file generates required arrays
            charge = np.zeros(potential0.shape)
          
        print('\n' + '''The parameters have been initialised as the following: \n
        Maximum Iterations: %s
        Point Separation (m): %s 
        Convergence Criterion (%%): %s ''' %(iterations, h, criterion)), # Prints out parameter values
        if inputselection == 'a': # Only prints out extra parameter settings if they are relevant
            print('''        Charge Density (C/m^3): %s
        Potential (V): %s
        x-length (m): %s
        y-length (m): %s
        Plate Length (m): %s
        Plate Separation (m): %s ''' %(Q, V, xlen, ylen, a, d)),
        
        paramselection = input('''Enter a choice: \n
        'a' (To keep these parameters),
        'b' (To change these parameters),
        'r' (To return to the previous menu): ''') # Allows user to change parameters
        print('\n' + 'You entered the choice: %s \n' % paramselection)

        if paramselection == 'r':
            return 'r'
        
        elif paramselection not in ['a', 'b']:
            print('\n' + 'This is not a valid choice. \n')
            return
            
        elif paramselection == 'b': # Runs 'ParamSet' if user wants to change inputs
            params = ParamSet(params, sections, 'Task 1', inputselection)
            [iterations, Q, V, xlen, ylen, h, a, d, criterion] = params 
        
    if inputselection == 'a': # Generates required variables (if not previously set)  
        Nx = int(xlen / h)
        Ny = int(ylen / h)
        
    elif inputselection == 'b':
        xlen = Nx * h
        ylen = Ny * h
            
    x = np.linspace(0, xlen, Nx) # Generates arrays for plotting
    y = np.linspace(0, ylen, Ny)
    xv, yv = np.meshgrid(x, y[::-1])
    N = [Ny, Nx]
    P = [iterations, Ny, Nx]
    
    if inputselection == 'a': # Generates required arrays (if not previously set) 
        charge, setvalues, potential0 = np.zeros(N), np.zeros(N), np.zeros(N) 
        if Poisson and Menu in ['On', 'Off']:
            charge = CapacitorPoisson(charge, a, d, h, N, Q)
        elif Menu in ['On', 'Off']:
            potential0, setvalues = CapacitorLaplace(potential0, setvalues, a, d, h, N, V)
        else: # For testing convergence - uses a more random array (not a capacitor)
            setvalues, potential0 = np.zeros(N), np.random.rand(Ny, Nx) * 10
            potential0[0, 0], potential0[0, -1], potential0[-1, 0], potential0[-1, -1] = np.mean(potential0), np.mean(potential0), np.mean(potential0), np.mean(potential0) 
            setvalues[0, 0], setvalues[0, -1], setvalues[-1, 0], setvalues[-1, -1] = 1, 1, 1, 1
              
    potential, electricfield, Ex, Ey = np.zeros(P), np.zeros(P), np.zeros(P), np.zeros(P)
    potential[0] = potential0    
    
    electricfield[0] = EField(potential[0], h, N)
    grad = np.gradient(potential[0])
    Ey[0], Ex[0] = grad[0], - grad[1]
    
    params = [iterations, charge, potential, electricfield, setvalues, Ey, Ex, h, N, criterion]   
    [potential, electricfield, Ey, Ex, n] = Relaxation(params, Gauss) # Runs the relaxation function for given parameters and settings

    params = [potential, electricfield, xlen, ylen, y, h, Nx]
    
    if Gif: # Produces a GIF of the plots with increasing iteration count
        jlist = []
        plt.ioff()
        results_dir = Directory('Task 1 GIFs')
        for j in np.linspace(0, n, 100): # Generates plots for j iterations
            if int(j) not in jlist:
                jlist.append(int(j)) # Saves plots to specified folder
                Task1Plots(params, int(j), results_dir)
        
        images = []
        try:
            for filename in jlist: # Compiles plots in a folder into a GIF
                images.append(imageio.imread(results_dir + str(filename) + '.png'))
        except OSError:
            print('A file could not be found.')
        imageio.mimsave(results_dir + 'Potential.gif', images)
        plt.ion()
    
    if CSV: # Saves data to .csv file
        FileWrite('Task1.csv' %h, params)

    if Singlegraph: # Plots final state of arrays
        f, ax1 = plt.subplots(1, 1) 
        M = np.hypot(Ex[n], Ey[n])
        ax1.quiver(xv, yv, Ex[n], Ey[n], M, pivot = 'mid')
        ax1.set_title('Electric Field', size = 16)
        ax1.set_xlabel('x (m)', fontsize = 10)
        ax1.set_ylabel('y (m)', fontsize = 10)
        ax1.tick_params(labelsize = 8)
        ax1.set_xlim(0, xlen)
        ax1.set_ylim(0, ylen)
        
        Task1Plots(params, n, None)
    
    if Multigraph: # Plots 1D slices of arrays for multiple numbers of iterations on same axes
        f, (ax1, ax2) = plt.subplots(2, 1, figsize = (10, 10), sharex = True)       
        for j in np.linspace(0, n, 5): # [0, 100, 400, 1000, 3000]: #
            ax1.plot(y[::-1], potential[int(j), :, Nx // 2], lw = 1, label = '%s' %(int(j)))
            ax2.plot(y[::-1], electricfield[int(j), :, Nx // 2], lw = 1, label = '%s' %(int(j)))
    
        ax1.set_title('Potential', size = 16)
        ax1.set_ylabel('Potential (V) at x = %s m' %(xlen / 2), fontsize = 10)
        ax1.tick_params(labelsize = 8) 
        ax1.legend(loc = 'best')

        ax2.set_title('Electric Field', size = 16)
        ax2.set_xlabel('y (m)', fontsize = 10)
        ax2.set_ylabel('Electric Field (V/m) at x = %s m' %(xlen / 2), fontsize = 10)
        ax2.tick_params(labelsize = 8)
        ax2.legend(loc = 'best')
    
    if Menu != 'On': # Returns parameters for testing
        return [potential, electricfield, Ey, Ex, n]
    
    plt.show()
    return 'r' # Exits function - returns to previous menu

# -------------- RELAXATION PHYSICS CODE --------------  

def EField(pnew, h, N): # Calaculates the gradient in potential at each point
    '''
    Calculates the magnitude of the electric field at each point on the grid
    '''
    Field = np.zeros(N)
    for j in range(N[0]):
        for i in range(N[1]):
            [Ex, Ey] = [[], []]
            if j != 0:
                Ey.append(pnew[j, i] - pnew[j - 1, i])
            if j != N[0] - 1:
                Ey.append(pnew[j + 1, i] - pnew[j, i])
            if i != 0:
                Ex.append(pnew[j, i] - pnew[j, i - 1])
            if i != N[1] - 1:
                Ex.append(pnew[j, i + 1] - pnew[j, i])
            E = [sum(Ey) / (2 * h), sum(Ex) / (2 * h)]
            Field[j, i] = (E[0] ** 2 + E[1] ** 2) ** 0.5
    return Field # Returns the magnitude of the electric field across the grid

def CapacitorPoisson(pvalues, a, d, h, N, Q): # Simulates a capacitor using a grid of charge
    '''
    Creates a grid of charge which simulates a capacitor
    '''
    caplen = a
    yloc = [- d / 2, d / 2]
    xloc = [0, 0]
    capx1 = np.arange(int(N[1] / 2 - caplen / (2 * h) + xloc[0] / h), int(N[1] / 2 + caplen / (2 * h) + xloc[0] / h))
    capx2 = np.arange(int(N[1] / 2 - caplen / (2 * h) + xloc[1] / h), int(N[1] / 2 + caplen / (2 * h) + xloc[1] / h))
    for i in capx1:
        pvalues[int(N[0] / 2 + yloc[0] / h), i] = - Q / 2 # (8.85 * 10 ** (-12))
    for i in capx2:
        pvalues[int(N[0] / 2 + yloc[1] / h) - 1, i] = Q / 2 # (8.85 * 10 ** (-12))
    return pvalues

def CapacitorLaplace(pvalues, fixedV, a, d, h, N, V): # Simulates a capacitor by fixing the potential on the plates
    '''
    Creates a grid of potential which simulates a capacitor
    '''
    caplen = a
    yloc = [- d / 2, d / 2]
    xloc = [0, 0]
    capx1 = np.arange(int(N[1] / 2 - caplen / (2 * h) + xloc[0] / h), int(N[1] / 2 + caplen / (2 * h) + xloc[0] / h))
    capx2 = np.arange(int(N[1] / 2 - caplen / (2 * h) + xloc[1] / h), int(N[1] / 2 + caplen / (2 * h) + xloc[1] / h))
    for i in capx1:
        pvalues[int(N[0] / 2 + yloc[0] / h), i] = - V / 2 # Sets the potential at a point
        fixedV[int(N[0] / 2 + yloc[0] / h), i] = 1 # Sets that point as a boundary condition
    for i in capx2:
        pvalues[int(N[0] / 2 + yloc[1] / h), i] = V / 2
        fixedV[int(N[0] / 2 + yloc[1] / h), i] = 1
    return pvalues, fixedV
    
def Relaxation(params, Gauss):
    '''
    Uses finite-difference to 'relax' into a solution to Laplace's or Poisson's equation
    '''
    [iterations, charge, potential, electricfield, setvalues, Ey, Ex, h, N, criterion] = params
    test = 0

    print('\n' + 'The maximum number of iterations is: ' + str(iterations) + '\n')
    for n in range(iterations):
        if Gauss:
            potential[n + 1] = potential[n].copy() # Makes the new grid a copy of the old
            potential[n + 1] = GaussSeidel(potential[n + 1], charge, h, N) # Runs Gauss-Seidel for the new grid
        else:
            potential[n + 1] = Jacobi(potential[n], potential[n + 1], charge, h, N) # Runs Jacobi for the old and new grids
        for j in range(potential[n + 1].shape[0]):
            for i in range(potential[n + 1].shape[1]):
                if setvalues[j, i] == 1: # Checks for boundary conditions
                    potential[n + 1][j, i] = potential[0][j, i] # Resets if boundary conditions
        electricfield[n + 1] = EField(potential[n + 1], h, N)
        grad = np.gradient(potential[n + 1]) # Finds the electric field
        Ey[n + 1], Ex[n + 1] = grad[0], - grad[1]           
        if Convergence(potential[n], potential[n + 1], N, n, iterations, criterion):
            break
        
        if n - test >= 10: # Stops printing every iterations
            test = n # Prints out the number of iterations completed
            sys.stdout.write('\r' + 'Approximately %s iterations completed..'  % n)
            sys.stdout.flush()    
    return [potential, electricfield, Ey, Ex, n]

def Jacobi(pold, pnew, charge, h, N):
    '''
    Runs the Jacobi method for a grid
    '''
    for j in range(N[0]):
        for i in range(N[1]):
            V = []
            if j != 0:
                V.append(pold[j - 1, i])
            if j != N[0] - 1:
                V.append(pold[j + 1, i])
            if i != 0:
                V.append(pold[j, i - 1])
            if i != N[1] - 1:
                V.append(pold[j, i + 1])
            if len(V) != 0:
                pnew[j, i] = sum(V) / len(V)
            pnew[j, i] += (charge[j, i] * h ** 2) / 4 # Allows Poisson's equation to be run
    return pnew

def GaussSeidel(pnew, charge, h, N):
    '''
    Runs the Gauss-Seidel method for a grid
    '''
    for j in range(N[0]):
        for i in range(N[1]):
            V = []
            if j != 0:
                V.append(pnew[j - 1, i])
            if j != N[0] - 1:
                V.append(pnew[j + 1, i])
            if i != 0:
                V.append(pnew[j, i - 1])
            if i != N[1] - 1:
                V.append(pnew[j, i + 1])
            if len(V) != 0:
                pnew[j, i] = sum(V) / len(V)
            pnew[j, i] += (charge[j, i] * h ** 2) / 4 # Allows Poisson's equation to be run
    return pnew

# -------------- RELAXATION PLOTTING --------------  

def Task1Plots(params, j, results_dir): # These plots were being used a few times - function reduces code
    '''
    Generates a set of four plots for the relaxation section
    '''
    [potential, electricfield, xlen, ylen, y, h, Nx] = params

    f, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2, figsize = (20, 10))  
    img1 = ax1.imshow(potential[j], extent=[0, xlen, 0, ylen]) # cmap = 'PuOr' - can help with testing as can seen where zero is more easily
    ax1.set_title('Potential', size = 16)
    ax1.set_xlabel('x (m)', fontsize = 10)
    ax1.set_ylabel('y (m)', fontsize = 10)
    ax1.tick_params(labelsize = 8) 
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes('right', size = '5%', pad = 0.05)
    cax1.set_title('(V)', fontsize = 10)
    f.colorbar(img1, cax = cax1)
    cax1.tick_params(labelsize = 8)
    
    img2 = ax2.plot(y[::-1], potential[j, :, Nx // 2])
    ax2.set_xlabel('y (m)', fontsize = 10)
    ax2.set_ylabel('Potential (V) at x = %s m' %(xlen / 2), fontsize = 10)
    ax2.tick_params(labelsize = 8) 

    img3 = ax3.imshow(electricfield[j], extent=[0, xlen, 0, ylen]) 
    ax3.set_title('Electric Field', size = 16)
    ax3.set_xlabel('x (m)', fontsize = 10)
    ax3.set_ylabel('y (m)', fontsize = 10)
    ax3.tick_params(labelsize = 8) 
    divider = make_axes_locatable(ax3)
    cax3 = divider.append_axes('right', size = '5%', pad = 0.05)
    cax3.set_title('(V/m)', size = 10)
    f.colorbar(img3, cax = cax3)
    cax3.tick_params(labelsize = 8)
    
    img4 = ax4.plot(y[::-1], electricfield[j, :, Nx // 2])
    ax4.set_xlabel('y (m)', fontsize = 10)
    ax4.set_ylabel('Electric Field (V/m) at x = %s m' %(xlen / 2), fontsize = 10)
    ax4.tick_params(labelsize = 8)

    plt.tight_layout()
    plt.subplots_adjust(left = 0.1, top = 0.9, wspace = 0.3, right  = 0.9, bottom = 0.1)

    if results_dir == Directory('Task 1 GIFs'): # Saves plots to folder for GIF making
        plt.savefig(results_dir + str(j))
        plt.close('all')
        
# -------------- DIFFUSION MENU -------------- 
    
def Task2(params, sections): # Base structure for task 2
    '''
    Provides a menu system for Task 2 (the diffusion section)
    '''
    [t, dt, k, c, p, xlen, ylen, h, criterion] = params 
    [Menu, Gauss, Gif, CSV, Singlegraph, Multigraph] = sections
    inputselection = 'a' 
    
    if Menu == 'On':  
        inputselection = input('''Enter a choice: \n
        'a' (To simulate the Furnace),
        'b' (To simulate the Furnace with heat loss),
        'c' (To input a different array): ''') # Allows the user to choose the section to run from within the console
        print('\n' + 'You entered the choice: %s \n' % inputselection)
        
        if inputselection not in ['a', 'b', 'c']:
            print('\n' + 'This is not a valid choice. \n')
            return
                 
        elif inputselection == 'c': # Prompts user to create and import .csv file
            print('\n' + 'Please create a .csv file with the sought after potential distribution.')
            phi0 = CSVImport(None)
            Nx, Ny = phi0.shape[1], phi0.shape[0]
            print('\n' + "Please create a .csv file for the boundary conditions. Place '1' at any points to remain unchanged and '0' elsewhere.")
            setvalues = CSVImport(phi0)
    
        print('\n' + '''The parameters have been initialised as the following: \n
        End Time (s): %s
        dt (s): %s
        Point Separation (m): %s
        k (W/m/K): %s
        c (J/kg/K): %s
        p (kg/m^3): %s 
        Convergence Criterion (%%): %s''' %(t, dt, h, k, c, p, criterion)) # Prints out parameter values
        if inputselection == 'a': # Only prints out extra parameter settings if they are relevant
            print('''        x-length (m): %s
        y-length (m): %s ''' %(xlen, ylen))
         
        paramselection = input('''Enter a choice: \n
        'a' (To keep these parameters),
        'b' (To change these parameters),
        'r' (To return to the previous menu): ''')
        print('\n' + 'You entered the choice: %s \n' % paramselection)
    
        if paramselection == 'r':
            return 'r'
        
        elif paramselection not in ['a', 'b', 'r']:
            print('\n' + 'This is not a valid choice. \n')
            return
            
        elif paramselection == 'b':
            params = ParamSet(params, sections, 'Task 2', inputselection)   
            [t, dt, k, c, p, xlen, ylen, h, criterion] = params
    
    iterations = int(t / dt)
    a = k / (c * p)
    
    if inputselection in ['a', 'b']:
        Nx = int(xlen / h)
        Ny = int(ylen / h)
        
    elif inputselection == 'c':
        xlen = Nx * h
        ylen = Ny * h
        
    N = [Ny, Nx]
    Nmag = Ny * Nx
    x = np.arange(0, xlen, h)
    vect = np.zeros((iterations, Nmag))
    phi = np.zeros((iterations, Ny, Nx))
    params = [dt, a, h, Nmag, Ny, Nx]
    matrix = MatrixDefine(params)
    
    if inputselection == 'a': # Diffusion with no heat loss
        phi[0], setvalues = IronRod1(phi[0], N)
    
    elif inputselection == 'b': # Diffusion with heat loss 
        phi[0], setvalues = IronRod2(phi[0], N)
    
    elif inputselection == 'c': # Diffusion for a user inputted array
        phi[0] = phi0
    
    vect[0] = phi[0].flatten()
    solvmatrix = np.linalg.inv(matrix)

    params = [iterations, setvalues, solvmatrix, vect, phi, Ny, Nx, N, criterion]     
    [phi, n] = Diffusion(params)

    params = [phi, xlen, ylen, x, Ny]
            
    if Gif:
        jlist = []
        plt.ioff()
        results_dir = Directory('Task 2 GIFs')
        for j in np.linspace(0, n, 100):
            if int(j) not in jlist:
                Task2Plots(params, int(j), results_dir)
                jlist.append(int(j))
        
        images = []
        try:
            for filename in jlist:
                images.append(imageio.imread(results_dir + str(filename) + '.png'))
        except OSError:
            print('A file could not be found.')
        imageio.mimsave(results_dir + 'IronBar.gif', images)
        plt.ion()
        
    if CSV:
        FileWrite('Task2' %h, params)
    
    if Singlegraph:        
        Task2Plots(params, n, None)
    
    if Multigraph:  
        f, ax1 = plt.subplots(1, 1, figsize = (5, 5))    
        for j in np.linspace(0, n , 5):  # [0, 300, 1000, 2000, 10000]: # [0, 1000, 4000, 10000, 30000]:
            ax1.plot(x, phi[int(j), Ny // 2], lw = 1, label = '%s' %(int(j)))
            
        ax1.set_title('Temperature', size = 16)
        ax1.set_xlabel('x (m)', fontsize = 10)
        ax1.set_ylabel('Temperature (C) at y = %s m' %(ylen / 2), fontsize = 10)
        ax1.tick_params(labelsize = 8) 
        ax1.legend(loc = 'best')
        
    if Menu != 'On':
        return [phi, n]
        
    plt.show()
    return 'r'

# -------------- DIFFUSION PHYSICS CODE --------------

def IronRod1(pvalues, N):
    '''
    Initialises grid for iron rod with no heat loss
    '''
    setvalues = np.zeros(N)
    for j in range(N[1]):
        pvalues[:, j] = 20
    pvalues[:, N[1] - 1], setvalues[:, N[1] - 1] = 1000, 1
    return pvalues, setvalues

def IronRod2(pvalues, N):
    '''
    Initialises grid for iron rod with heat loss
    '''
    setvalues = np.zeros(N)
    for j in range(N[1]):
        pvalues[:, j] = 20
    pvalues[:, 0], setvalues[:, 0] = 0, 1
    pvalues[:, N[1] - 1], setvalues[:, N[1] - 1] = 1000, 1
    return pvalues, setvalues

def Diffusion(params):
    '''
    Iterates via the implicit method to simulate heat diffusion
    '''
    [iterations, setvalues, solvmatrix, vect, phi, Ny, Nx, N, criterion] = params
    test = 0
    
    print('\n' + 'The maximum number of iterations is: ' + str(iterations) + '\n')
    for n in range(iterations):
        vect[n + 1] = np.dot(solvmatrix, vect[n])
        for i in range(len(vect[n + 1])):
            if setvalues.flatten()[i] == 1:
                vect[n + 1][i] = vect[0][i]
        phi[n + 1] = vect[n + 1].reshape(Ny, Nx)
        if Convergence(phi[n], phi[n + 1], N, n, iterations, criterion):
            break
        
        if n - test >= 10:
            test = n
            sys.stdout.write('\r' + 'Approximately %s iterations completed..' % n)
            sys.stdout.flush()
    return [phi, n]
    
def MatrixDefine(params):
    '''
    Defines the matrix for the implicit method
    '''
    [dt, a, h, Nmag, Ny, Nx] = params
    matrix = np.zeros((Nmag, Nmag))
    # Allows 2D diffusion to be simulated
    for j in range(Ny):
        for i in range(Nx):
            k = j * Nx + i
            # Iterates through points in the matrix and inputs values
            matrix[(k ,k)] = (1 + (4 * a * dt) / (h ** 2))
            # 2D diffusion requires extra terms
            if i < Nx - 1:
                matrix[(k, k + 1)] = - (a * dt) / (h ** 2)
            if k < Nmag - Nx:
                matrix[(k, k + Nx)] = - (a * dt) / (h ** 2)
            if j in [0, Ny - 1] or i in [0, Nx - 1]:
                matrix[(k ,k)] = (1 + (3 * a * dt) / (h ** 2))
            if [j, i] in [[0, 0], [0, Nx - 1], [Ny - 1, 0], [Ny - 1, Nx - 1]]:
                matrix[(k ,k)] = (1 + (2 * a * dt) / (h ** 2))
            if i > 0:
                matrix[(k, k - 1)] = - (a * dt) / (h ** 2)
            if k >= Nx:
                matrix[(k, k - Nx)] = - (a * dt) / (h ** 2)
    return matrix

# -------------- DIFFUSION PLOTTING -------------- 
        
def Task2Plots(params, j, results_dir):
    '''
    Generates a set of two plots for the diffusion section
    '''
    [phi, xlen, ylen, x, Ny] = params
    f, (ax1, ax2) = plt.subplots(2, 1 , figsize = (10, 10))
    img1 = ax1.imshow(phi[j], extent=[0, xlen, 0, ylen], cmap = 'inferno')
    ax1.set_aspect('auto')
    ax1.set_title('Temperature', size = 16)
    ax1.set_xlabel('x (m)', fontsize = 10)
    ax1.set_ylabel('y (m)', fontsize = 10)
    ax1.tick_params(labelsize = 8)
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes('right', size = '5%', pad = 0.05)
    cax1.set_title('(C)', size = 10)
    f.colorbar(img1, cax = cax1)
    cax1.tick_params(labelsize = 8)
    
    img2 = ax2.plot(x, phi[j, Ny // 2], lw = 1)
    ax2.set_xlabel('x (m)', fontsize = 10)
    ax2.set_ylabel('Temperature (C) at y = %s m' %(ylen / 2), fontsize = 10)
    ax2.tick_params(labelsize = 8) 
    
    plt.tight_layout()
    plt.subplots_adjust(left = 0.1, top = 0.9, hspace = 0.3, right  = 0.9, bottom = 0.1)
    
    if results_dir == Directory('Task 2 GIFs'):
        plt.savefig(results_dir + str(j))
        plt.close('all')
        
# -------------- RUN MENU -------------- 

np.seterr(divide = 'ignore', invalid = 'ignore')
taskSelection = 0 # While True runs Exercise 2
variables = ParamSet(None, None, 'Initial', None)
while taskSelection != 'q':
    taskSelection, variables[0] = Exercise2(variables)
  
# -------------- EXTRAS -------------- 
    
'''
The following is not part of the main code and was only used to generate the plots seen in the report
'''
    
# ------------------------------------ 

def TimeTest(params1, params2, params3):
    '''
    Runs tests to determine the time and iteration count for methods to converge
    '''
    Nvals = np.linspace(10, 30, 11)
    hvals = 1 / Nvals
    [Q, V, a, d] = params1
    [k, c, p] = params2
    [iterations, xlen, ylen, h, criterion] = params3
    sections = ['Test', False, False, False, False, False]
    xlen = ylen = 1
    
    repeats = 3
    total_time, std_time, total_n, std_n = [], [], [], []
    t = 10
    dt = t / iterations
    
    taskselection = 'a'
   
    for h in hvals:    
        stat1_time = np.zeros(repeats)
        stat2_time = np.zeros(repeats)
        stat_n = np.zeros(repeats)    
        if taskselection == 'a': 
            for j in range(repeats):
                print('\n' + 'N is: %s, j is: %s' %(1 / h, j))
                params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
                stat1_time[j] = time.time()
                [potential, electricfield, Ey, Ex, n] = Task1(params, sections, False)
                stat2_time[j] = time.time()
                stat_n[j] = n
                
        elif taskselection == 'b': 
            for j in range(repeats):
                print('\n' + 'N is: %s, j is: %s' %(1 / h, j))
                params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
                stat1_time[j] = time.time()
                [potential, electricfield, Ey, Ex, n] = Task1(params, sections, True)
                stat2_time[j] = time.time()
                stat_n[j] = n
            
        elif taskselection == 'c':   
            for j in range(repeats):
                params = [t, dt, k, c, p, xlen, ylen, h, criterion]
                stat1_time[j] = time.time()
                [phi, n] = Task2(params, sections)   
                stat2_time[j] = time.time()
                stat_n[j] = n
                
        stat_time = stat2_time - stat1_time
        total_time.append(np.mean(stat_time))
        std_time.append(np.std(stat_time))
        total_n.append(np.mean(stat_n))
        std_n.append(np.std(stat_n))
            
    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.errorbar(Nvals, total_time, xerr = 0, yerr = std_time, linestyle = 'None', fmt = 'o', ms = 2)
    ax2.errorbar(Nvals, total_n, xerr = 0, yerr = std_n, linestyle = 'None', fmt = 'o', ms = 2)
    FileWrite('TimeTest.csv', [Nvals, total_time, std_time])
    FileWrite('IterationTest.csv', [Nvals, total_n, std_n])   
    
    ax1.set_title('Grid Density', size = 16)
    ax1.set_xlabel('Grid Density in 1D (m$^{-1}$)', fontsize = 10)
    ax1.set_ylabel('Time to Converge (s)', fontsize = 10)
    ax1.tick_params(labelsize = 8)
    
    ax2.set_xlabel('Grid Density in 1D (m$^{-1}$)', fontsize = 10)
    ax2.set_ylabel('Iterations to Converge', fontsize = 10)
    ax2.tick_params(labelsize = 8)
    
    plt.tight_layout()
    plt.subplots_adjust(left = 0.1, top = 0.9, wspace = 0.3, right  = 0.9, bottom = 0.1)
    
def InfinitePlate(params):
    '''
    Runs tests to check the inifinte plate solution
    '''
    dvals = np.linspace(0.1, 0.9, 9)
    [iterations, Q, V, xlen, ylen, h, a, d, criterion] = params
    sections = ['Off', False, False, False, False, False]
    tvals = V / dvals
    
    evals = []   
    for d in dvals:
        params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
        [potential, electricfield, Ey, Ex, n] = Task1(params, sections, False)
        evals.append(electricfield[n][int(electricfield.shape[1] / 2)][int(electricfield.shape[2] / 2)])
    
    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(a / dvals, abs(evals - tvals), linestyle = 'None', marker = 'x', ms = 4)
    ax1.plot([min(a / dvals), max(a / dvals)], [0, 0], linestyle = '--')
    ax1.set_title('Infinite Plate Capacitor', size = 16)
    ax1.set_xlabel('a/d', fontsize = 16)
    ax1.set_ylabel('Distance Between V/d and Measured Value (Vm$^{-1}$)', fontsize = 10)
    ax1.tick_params(labelsize = 8)
    
    ax2.plot(a / dvals, abs(evals - tvals), linestyle = 'None', marker = 'x', ms = 4)
    ax2.set_title('Infinite Plate Capacitor', size = 16)
    ax2.set_xlabel('a/d', fontsize = 16)
    ax2.set_ylabel('Distance Between V/d and Measured Value (Vm$^{-1}$)', fontsize = 10)
    ax2.set_yscale('log', nonposy = 'clip')
    ax2.tick_params(labelsize = 8)
    
    FileWrite('InfinitePlate1.csv', [dvals, evals])
    
def Analytical(params1, params2, params3):
    '''
    Runs tests to check if the Jacobi method relaxes to an analytical solution
    '''
    [Q, V, a, d] = params1
    [k, c, p] = params2
    [iterations, xlen, ylen, h, criterion] = params3    
    a = k / (c * p)
        
    Nx = int(xlen / h)
    Ny = int(ylen / h)
    
    N = [Ny, Nx]
    P = [iterations, Ny, Nx]
    
    setvalues, charge, test = np.zeros(N), np.zeros(N), np.zeros(N)
    setvalues[:, 0], setvalues[:, -1], setvalues[0], setvalues[-1] = 1, 1, 1, 1
    potential0 = np.zeros((N))
    potential0[:, 0], potential0[:, -1], potential0[0], potential0[-1]  = 100, 0, 0, 0
    potential, electricfield, Ex, Ey = np.zeros(P), np.zeros(P), np.zeros(P), np.zeros(P)
    potential[0] = potential0     
    params = [iterations, charge, potential, electricfield, setvalues, Ey, Ex, h, N, criterion] 
    [potential, electricfield, Ey, Ex, n] = Relaxation(params, False)
    y = np.linspace(0, ylen, Ny)
    x = np.linspace(0, xlen, Nx)
    for j in range(Ny):
        for i in range(Nx):
            for m in range(1, 201, 2):
                a = np.sin((np.pi * m * y[j]) / ylen)
                b = np.sinh((np.pi * m * (x[i] - xlen)) / ylen)
                c = - 4 * 100 / (np.pi * m * np.sinh((np.pi * m * xlen) / ylen))
                test[j, i] +=  a * b * c
    
    f, (ax1, ax2) = plt.subplots(2, 1, figsize = (5, 10))
    img1 = ax1.imshow(potential[n], extent = [0, xlen, 0, ylen])
    ax1.set_xlabel('x (m)', fontsize = 10)
    ax1.set_ylabel('y (m)', fontsize = 10)
    ax1.tick_params(labelsize = 8)
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes('right', size = '5%', pad = 0.05)
    cax1.set_title('(V)', size = 10)
    f.colorbar(img1, cax = cax1)
    cax1.tick_params(labelsize = 8)
    
    img2 = ax2.imshow(potential[n] - test, extent = [0, xlen, 0, ylen])
    ax2.set_xlabel('x (m)', fontsize = 10)
    ax2.set_ylabel('y (m)', fontsize = 10)
    ax2.tick_params(labelsize = 8)
    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes('right', size = '5%', pad = 0.05)
    cax2.set_title('(V)', size = 10)
    f.colorbar(img2, cax = cax2)
    cax2.tick_params(labelsize = 8)
    
    plt.tight_layout()
    plt.subplots_adjust(left = 0.1, top = 0.9, hspace = 0.3, right  = 0.9, bottom = 0.1)
    
def SlicePlot(params1, params2, params3):
    '''
    Plots a 2D array with a cross section of the paramater against iteration count 
    '''
    sections = ['Test', False, False, False, False, False]
    [Q, V, a, d] = params1
    [k, c, p] = params2
    [iterations, xlen, ylen, h, criterion] = params3
    t = 10000
    dt = t / iterations
    
    taskselection = 'c'
    f, ax1 = plt.subplots(1, 1, figsize = (10, 10)) 
    
    if taskselection == 'a':
        params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
        [potential, electricfield, Ey, Ex, n] = Task1(params, sections, False)
        ax1.imshow(potential[:, :, potential.shape[2] // 2], extent = [0, xlen, 0, xlen])
        
    elif taskselection == 'b': 
        params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
        [potential, electricfield, Ey, Ex, n] = Task1(params, sections, True)
        
    elif taskselection == 'c':
        params = [t, dt, k, c, p, xlen, ylen, h, criterion]
        [phi, n] = Task2(params, sections)   
        ax1.imshow(phi[:, phi.shape[2] // 2], extent = [0, xlen, 0, xlen])
    
    plt.tight_layout()
    plt.subplots_adjust(left = 0.1, top = 0.9, wspace = 0.3, right  = 0.9, bottom = 0.1)      
    
def ConvergenceTest(params1, params2, params3):
    '''
    Runs tests to determine the convergence of Jacobi and Gauss-Seidel with changing convergence criterion
    '''
    criteria = np.logspace(-12, 1, 27)
    [Q, V, a, d] = params1
    [k, c, p] = params2
    [iterations, xlen, ylen, h, criterion] = params3

    t = 10
    dt = t / iterations

    taskselection = 'b'
    f, (ax1, ax2) = plt.subplots(2, 1, figsize = (5, 10)) 

    for sections in [['Off', False, False, False, False, False], ['Off', True, False, False, False, False]]:
        n_list, diff_list = [], []
        
        if taskselection == 'a':
            params = [iterations, Q, V, xlen, ylen, h, a, d, -1]
            [potentialtrue, electricfieldtrue, Eytrue, Extrue, ntrue] = Task1(params, sections, False)
            
        elif taskselection == 'b':
            params = [iterations, Q, V, xlen, ylen, h, a, d, -1]
            [potentialtrue, electricfieldtrue, Eytrue, Extrue, ntrue] = Task1(params, sections, True)
            
        elif taskselection == 'c':
            params = [t, dt, k, c, p, xlen, ylen, h, -1]
            [phitrue, ntrue] = Task2(params, sections)   
        
        for criterion in criteria:
            print('\n' + 'The value of the criterion is: %s' %(criterion) + '\n')
            if taskselection == 'a':
                params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
                [potential, electricfield, Ey, Ex, n] = Task1(params, sections, False)
                diff_list.append(np.linalg.norm(abs(potential[n] - potentialtrue[ntrue])) * 100 / np.linalg.norm(abs(potentialtrue[ntrue])))
                n_list.append(n)
                
            elif taskselection == 'b':
                params = [iterations, Q, V, xlen, ylen, h, a, d, criterion]
                [potential, electricfield, Ey, Ex, n] = Task1(params, sections, True)
                diff_list.append(np.linalg.norm(abs(potential[n] - potentialtrue[ntrue])) * 100 / np.linalg.norm(abs(potentialtrue[ntrue])))
                n_list.append(n)
                
            elif taskselection == 'c':
                params = [t, dt, k, c, p, xlen, ylen, h, criterion]
                [phi, n] = Task2(params, sections)   
                diff_list.append(np.linalg.norm(abs(phi[n] - phitrue[ntrue])) * 100 / np.linalg.norm(abs(phitrue[ntrue])))
                n_list.append(n)
                
        if sections[1]:
            value = 'Gauss-Seidel'
        else:
            value = 'Jacobi'

        ax1.plot(criteria, n_list, label = value)
        ax2.plot(criteria, diff_list, label = value)

        FileWrite('%s.csv' %(value), [criteria, n_list, diff_list])
        
        if taskselection == 'c':
            break
        
    ax1.invert_xaxis()
    ax1.set_title('Convergence', size = 16)
    ax1.set_xlabel('Convergence Criterion (%)', fontsize = 10)
    ax1.set_ylabel('Iterations to Converge', fontsize = 10)
    ax1.tick_params(labelsize = 8)
    ax1.set_xscale('log', nonposy = 'clip')
    ax1.legend(loc = 'best')
                
    ax2.invert_xaxis()
    ax2.set_xlabel('Convergence Criterion (%)', fontsize = 10)
    ax2.set_ylabel('Magnitude of Error (%)', fontsize = 10)
    ax2.tick_params(labelsize = 8)
    ax2.set_xscale('log', nonposy = 'clip')
    ax2.set_yscale('log', nonposy = 'clip')
    ax2.legend(loc = 'best')

'''
Uncomment this code to run the various functions
Warning - Changing the set parameter may cause the program to crash
'''
# SlicePlot([20, 2000, 1, 0.2], [59, 450, 7900], [10000, 1, 1, 0.02, 0])
# Analytical([20, 2000, 1, 0.2], [59, 450, 7900], [1000, 1, 1, 0.02, 0.01])
# TimeTest([20, 2000, 1, 0.2], [59, 450, 7900], [10000, 1, 1, 0.05, 0.1])
# ConvergenceTest([20, 2000, 1, 0.2], [59, 450, 7900], [10000, 1, 1, 0.05, 0.01])
# InfinitePlate([10000, 20, 2000, 2, 1, 0.05, 1, 0.2, 0.5])
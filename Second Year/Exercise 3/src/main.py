"""
Created on Sun Feb  5 16:19:48 2017

@author: thomaswilliams
"""

# Please run in IPython

# Functions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, MaxNLocator
print(plt.style.available)

def Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints):
    
    def Input_Clear(value):
        [y0,v0,Cd,p0,A,t,g,m,h,N,k] = [None] * 11
        return float(eval(input(value))) 
    
    def Input_Test(value):
    
    # This function takes the allows each input to be checked for errors without having to write the code multiple times
   
        while True:
            try:
                Input = Input_Clear(value)
                if(value  != "Input a value for g: " and value  != "Input a value for the v0: " and Input < 0):
                    print(" ")
                    print("You must input a positive number")  
                    continue
                elif("dt" in value and Input <= 0 or "time" in value and Input <= 0):
                    print(" ")
                    print("You must input a value greater than zero")
                    continue
                elif("dt" in value and Input > t):
                    print(" ")
                    print("dt must be less than the length of time")
                    continue
                elif(value  == "Input a value for the smallest dt: " and Input > dti):
                    print(" ")
                    print("The smallest dt must be less than the largest dt")
                    continue
                elif(value  == "Input a value for the number of steps: " and Input % 1 != 0 ):
                    print(" ")
                    print("You must input an integer")
                    continue
                return Input
            except (Exception):
                print(" ")
                print("You must input a number")
    
    if Section_Input == "0":
        [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = [1000,0,1.0,1.2,0.7,0,9.8,110,7.64 * 10 ** 3,0,0,0,1000]
        print(" ")
        print("v0 has been set as %s, Cd has been set as %s, ρ0 has been set as %s, A has been set as %s, g has been set as %s, m has been set as %s and h has been set as %s." %(v0,Cd,p0,A,g,m,h))

        
    elif Section_Input == "h":
        if Selection == "a":
            value = "Input a value for Cd: "
            Cd = Input_Test(value)
            value = "Input a value for A: "
            A = Input_Test(value)
            value = "Input a value for m: "
            m = Input_Test(value)
        elif Selection == "b":
            value = "Input a value for the v0: "
            v0 = Input_Test(value)
            value = "Input a value for ρ0: "
            p0 = Input_Test(value)
            value = "Input a value for g: "
            g = Input_Test(value)
            value = "Input a value for h: "
            h = Input_Test(value)
            
    elif Section_Input != "c" and Section_Input != "g":
        value = "Input a value for the starting height: "
        y0 = Input_Test(value)
        if Section_Input == "b" and Selection == "a":
            value = "Input a time to evaluate the values at: "
        else:
            value = "Input a time to evaluate the jump up to: "
        t = Input_Test(value)
        value = "Input a value for dt: "
        dt = Input_Test(value)
    
    elif Selection == "a":
        print(" ")
        print("The starting height has been set at %s" % y0)
        value = "Input a time to evaluate the values at: "
        t = Input_Test(value)
        value = "Input a value for the largest dt: "
        dti = Input_Test(value)
        value = "Input a value for the smallest dt: "
        dtf = Input_Test(value)
        print(" ")
        print("The number of steps has been set at: %s" % NumPoints)
        
    elif Selection == "b":
        value = "Input a value for the starting height: "
        y0 = Input_Test(value)
        value = "Input a value for the number of steps: "
        NumPoints = int(Input_Test(value))

        
    return [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints]

def Function_Run(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input):
    while True:
        try:
            if SectionG_Input == "Runge" or SectionG_Input == "Test":
                [speed,distance,time,v,y,i,k,N] = Runge_Kutta(y0,v0,Cd,p0,A,t,g,m,h,dt)
            elif SectionG_Input == "Mod":
                [speed,distance,time,v,y,i,k,N] = Modified_Euler(y0,v0,Cd,p0,A,t,g,m,h,dt)
            else:
                if Section_Input != "c" and Section_Input != "g":
                    [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                [speed,distance,time,v,y,i,k,N] = Euler(y0,v0,Cd,p0,A,t,g,m,h,dt)
            return [speed,distance,time,v,y,i,k,N,t,dt]
        except OverflowError:
            print(" ")
            print("The values became too large to compute; please use smaller dt: ")
            continue

def Euler(y0,v0,Cd,p0,A,t,g,m,h,dt):
    N = int(t / dt)
    dt = t / N
    [v,y,speed,distance,time] = [[v0],[y0],[abs(v0)],[0.0],[0.0]]
    for i in range(1, N + 1):
        def k(y):
            if Section_Input == "e" or Section_Input == "f" or Section_Input == "g":
                return (Cd * p0 * np.e**(-y / h) * A) / 2
            else:
                return (Cd * p0 * A) / 2
        v.append(v[i - 1] - dt * (g + (k(y[i - 1]) / m) * abs(v[i - 1]) * v[i - 1]))
        y.append(y[i - 1] + dt * v[i - 1])
        speed.append(abs(v[i]))
        distance.append(y0 - y[i])
        time.append(dt * i)
        if y[i] < 0:
            break
    k = k(0)
    return [speed,distance,time,v,y,i,k,N]

def Modified_Euler(y0,v0,Cd,p0,A,t,g,m,h,dt):
    N = int(t / dt)
    dt = t / N
    [v,y,speed,distance,time] = [[v0],[y0],[abs(v0)],[0.0],[0.0]]
    for i in range(1, N + 1):
        def k(y):
            if Section_Input == "e" or Section_Input == "f" or Section_Input == "g":
                return (Cd * p0 * np.e**(-y / h) * A) / 2
            else:
                return (Cd * p0 * A) / 2  
        vmid = v[i - 1] - (dt / 2) * (g + (k(y[i - 1]) / m) * abs(v[i - 1]) * v[i - 1])
        ymid = y[i - 1] + (dt / 2) * v[i - 1]
        v.append(v[i - 1] - dt * (g + (k(ymid) / m) * abs(vmid) * vmid))
        y.append(y[i - 1] + dt * vmid)
        speed.append(abs(v[i]))
        distance.append(y0 - y[i])
        time.append(dt * i)
        if y[i] < 0:
            break
    k = k(0)
    return [speed,distance,time,v,y,i,k,N]

def Runge_Kutta(y0,v0,Cd,p0,A,t,g,m,h,dt):
    N = int(t / dt)
    dt = t / N
    [v,y,speed,distance,time] = [[v0],[y0],[abs(v0)],[0.0],[0.0]]
    for i in range(1, N + 1):
        def k(y):
            if Section_Input == "e" or Section_Input == "f" or Section_Input == "g":
                return (Cd * p0 * np.e**(-y / h) * A) / 2
            else:
                return (Cd * p0 * A) / 2
        v1 = v[i - 1]
        y1 = y[i - 1]
        vk1 = - (g + (k(y1) / m) * abs(v1) * v1)
        yk1 = v1

        v2 = v1 + (dt / 2) * vk1
        y2 = y1 + (dt / 2) * yk1
        vk2 = - (g + (k(y2) / m) * abs(v2) * v2)
        yk2 = v2
        
        v3 = v1 + (dt / 2) * vk2
        y3 = y1 + (dt / 2) * yk2
        vk3 = - (g + (k(y3) / m) * abs(v3) * v3)
        yk3 = v3
        
        v4 = v1 + dt * vk3
        y4 = y1 + dt * yk3
        vk4 = - (g + (k(y4) / m) * abs(v4) * v4)
        yk4 = v4

        v.append(v1 + (dt / 6) * (vk1 + 2 * vk2 + 2 * vk3 + vk4))
        y.append(y1 + (dt / 6) * (yk1 + 2 * yk2 + 2 * yk3 + yk4))
        speed.append(abs(v[i]))
        distance.append(y0 - y[i])
        time.append(dt * i)
        if y[i] < 0:
            break
    k = k(0)
    return [speed,distance,time,v,y,i,k,N]

def plot(x,y,xlabel,xunits,ylabel,yunits,ax):
    ax.plot(x,y, lw=2)
    ax.set_xlim([x[0],x[-1]])
    if xlabel == None:
        pass
    elif xunits == None:
        ax.set_xlabel("%s" %(xlabel))           
    else:
        ax.set_xlabel("%s $%s$" %(xlabel,xunits))
    if ylabel == "Height":
        ax.set_ylim([0,(max(y) * 1.2)])
    elif ylabel == None:
        pass
    elif yunits == None:
        ax.set_xlabel("%s")
    else:
        ax.set_ylabel("%s $%s$" %(ylabel,yunits))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    if Section_Input == "c" or Section_Input == "g":
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(numticks = 6))
    else:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-0,5))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
        
def Dt_Difference(function,y0,v0,Cd,p0,A,t,g,m,h):
    vdiff = [0.0] * (NumValues)
    ydiff = [0.0] * (NumValues)
    Nvalues = [0.0] * (NumValues)
    for dt in dtlist:
        j = dtlist.index(dt)
        [speed,distance,time,v,y,i,k,N] = function(y0,v0,Cd,p0,A,t,g,m,h,dt)
        if Section_Input == "c":
            vdiff[j] = abs(v[-1] - (v[0] - (m * g / k) ** 0.5 * np.tanh((k * g / m) ** 0.5 * t)))
            ydiff[j] = abs(y[-1] - (y[0] - (m / (2 * k)) * np.log((np.cosh((k * g / m) ** 0.5 * t)) ** 2)))
        else:
            SectionG_Input = "Test"
            [testspeed,testdistance,testtime,testv,testy,testi,testk,testN,testt,testdt] = Function_Run(y[0],v0,Cd,p0,A,t,g,m,h,dt * 0.01,dti,dtf,NumPoints,Section_Input,SectionG_Input)
            vdiff[j] = abs(v[-1] - testv[-1])
            ydiff[j] = abs(y[-1] - testy[-1])
        Nvalues[j] = N
        if i < N:
            print(" ")
            print("The simulation was terminated as the object hit the ground at %.2f seconds" %(time[i]))
            print(" ")
            print("Please use a smaller value of time")
            return[i,N]

    plot(dtlist,vdiff,None,None,"Velocity Difference","/ms^{-1}",ax1)
    plot(dtlist,ydiff,"dt","/s","Position Difference","/ms^{-1}",ax3)
    plot(Nvalues,vdiff,None,None,None,None,ax2)
    plot(Nvalues,ydiff,"N",None,None,None,ax4)
    return[i,N]
    
def figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9):
    
    SectionG_Input = "0"
    
    def Difference(speed,distance,time,i,dt,testspeed,testdistance,testdt):
        [vdiff,ydiff] = [[0.0],[0.0]]
        for j in range(1,i + 1):
            try:
                if Section_Input == "g":
                    tdiff = (dt / testdt)
                    vdiff.append(speed[j] - testspeed[int(tdiff * j)])
                    ydiff.append(distance[j] - testdistance[int(tdiff * j)])
                else:
                    vdiff.append(speed[j] - (m * g / k) ** 0.5 * np.tanh((k * g / m) ** 0.5 * time[j]))
                    ydiff.append(distance[j] - (m / (2 * k)) * np.log((np.cosh((k * g / m) ** 0.5 * time[j])) ** 2))
            except IndexError:
                del vdiff[i:]
                del ydiff[i:]
                del height[i:]
                del time[i:]
        return [height,vdiff,ydiff,time]
    
    SectionG_Input = "Standard"
    [speed,distance,time,velocity,height,i,k,N,t,dt] = Function_Run(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input)
    if Section_Input == "g":
        SectionG_Input = "Test"
        [testspeed,testdistance,testtime,testv,testy,testi,testk,testN,testt,testdt] = Function_Run(height[0],v0,Cd,p0,A,t,g,m,h,dt * 0.01,dti,dtf,NumPoints,Section_Input,SectionG_Input)
    else:
        [testspeed,testdistance,testdt] = [0.0,0.0,0.0]
    if Section_Input == "b" or Section_Input == "g":
        [y,vdiff,ydiff,time] = Difference(speed,distance,time,i,dt,testspeed,testdistance,testdt)
        plot(time,vdiff,"Time","/s","Speed Difference","/ms^{-1}",ax1)
        plot(time,ydiff,"Time","/s","Height Difference","/m",ax4)
    else:
        plot(time,velocity,"Time","/s","Speed","/ms^{-1}",ax1)
        plot(time,height,"Time","/s","Height","/m",ax4)
        plot(distance,velocity,"Distance Fallen","/m","Speed","/ms^{-1}",ax7)
    
    SectionG_Input = "Mod"
    [mspeed,mdistance,mtime,mvelocity,mheight,mi,mk,mN,mt,mdt] = Function_Run(height[0],v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input)
    if Section_Input == "b" or Section_Input == "g":
        [my,mvdiff,mydiff,mtime] = Difference(mspeed,mdistance,mtime,mi,mdt,testspeed,testdistance,testdt)
        plot(mtime,mvdiff,"Time","/s","Speed Difference","/ms^{-1}",ax2)
        plot(mtime,mydiff,"Time","/s","Height Difference","/m",ax5)
    else:
        plot(mtime,mvelocity,"Time","/s","Speed","/ms^{-1}",ax1)
        plot(mtime,mheight,"Time","/s","Height","/m",ax4)
        plot(mdistance,mvelocity,"Distance Fallen","/m","Speed","/ms^{-1}",ax7)
    
    SectionG_Input = "Runge"
    [rspeed,rdistance,rtime,rvelocity,rheight,ri,rk,rN,rt,rdt] = Function_Run(height[0],v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input)
    if Section_Input == "b" or Section_Input == "g":
        [ry,rvdiff,rydiff,rtime] = Difference(rspeed,rdistance,rtime,ri,rdt,testspeed,testdistance,testdt)
        plot(rtime,rvdiff,"Time","/s","Speed Difference","/ms^{-1}",ax3)
        plot(rtime,rydiff,"Time","/s","Height Difference","/m",ax6) 
    else:
        plot(rtime,rvelocity,"Time","/s","Speed","/ms^{-1}",ax1)
        plot(rtime,rheight,"Time","/s","Height","/m",ax4)
        plot(rdistance,rvelocity,"Distance Fallen","/m","Speed","/ms^{-1}",ax7)
        
    print(" ")
    print("""The simulation was terminated as the object hit the ground at: 
            %.2f seconds (Euler)
            %.2f seconds (Modified Euler)
            %.2f seconds (Runge-Kutta)""" %(time[-1],mtime[-1],rtime[-1]))
    
    plt.tight_layout()
    #plt.style.use('seaborn-deep')
    plt.show()
    
    print("""The maximum speed achieved during the descent was:
            %.2f metres per second (Euler)
            %.2f metres per second (Modified Euler)
            %.2f metres per second (Runge-Kutta)""" %(max(speed),max(mspeed),max(rspeed)))
    
# Loop Until Quit
      
Section_Input = "0"
[y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(0,0,0,0,0,0,0,0,0,0,0,0,0)

while Section_Input != "q":
    SectionG_Input="0"

    Section_Input = input("""Enter a choice:  
    'a' (To simulate a fall with fixed drag),
    'b' (To test the convergence over time with fixed drag),
    'c' (To test the convergence for changing dt with fixed drag),
    'd' (To find how long it takes the body to reach 90 percent of its terminal velocity with fixed drag), 
    'e' (To simulate a fall with varying drag),  
    'f' (To test the convergence over time with varying drag),
    'g' (To test the convergence for changing dt with varying drag),
    'h' (To change the jump parameters),
    'q' (To quit): """)
    print(" ")
    print("You entered the choice: ",Section_Input)
    
# Section A    
    
    if Section_Input =="a":
        print(" ")
        print("You have chosen part (a)")
            
        f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3,figsize = (15,12))
                
        figure(y0,v0,Cd,p0,A,t,g,m,h,dt,"a",ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9)
           
# Section B
           
    elif Section_Input == "b":
        print(" ")
        print("You have chosen part (b)")
        
        Selection = "0"
          
        while Selection != "r":
            Selection = input("""Enter a choice:
    'a' (To test the Euler method numerical values at a given time),
    'b' (To plot the difference in the values),
    'c' (To plot the difference in the values on the same graph),
    'r' (To return to the previous menu): """)
            print(" ")
            print("You entered the choice:",Selection)
            
            if Selection == "r":
                continue
            
            elif Selection == "a":
                [speed,distance,time,v,y,i,k,N,t,dt] = Function_Run(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input)
                if i < N and Selection == "a":
                    print(" ")
                    print("Please use a smaller value of time")
                    continue
                print("""
According to the function:
    The speed is: %.2f metres per second
    The distance fallen: %.2f metres""" %(v[-1],y[-1]))
                vtrue = v0 - (m * g / k) ** 0.5 * np.tanh((k * g / m) ** 0.5 * t)
                ytrue = y0 - (m / (2 * k)) * np.log((np.cosh((k * g / m) ** 0.5 * t)) ** 2)
                print("""
According to the model:
    The speed is: %.2f metres per second
    The distance fallen: %.2f metres""" %(abs(vtrue),ytrue))
                print("""
Therefore:
    The speed difference is: %.2g metres per second
    The height difference is: %.2g metres""" %(v[-1] - vtrue,y[-1] - ytrue))
                print(" ")
                
            elif Selection == "b":
                f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3,figsize = (15,8))
                figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9)
            
            elif Selection == "c":
                f, (ax1, ax2) = plt.subplots(2, 1,figsize = (5,8))
                figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax1,ax1,ax2,ax2,ax2,ax3,ax3,ax3)
                
            else:
                print(" ")
                print("This is not a valid choice")
        
# Section C
           
    elif Section_Input == "c":
        print(" ")
        print("You have chosen part (c)")
        
        Selection = "0"
        
        while Selection != "r":
            Selection = input("""Enter a choice:
    'a' (To plot the difference in the values against dt and N),
    'b' (To change the paramters of the plot),
    'r' (To return to the previous menu): """)
            print(" ")
            print("You entered the choice:",Selection)
      
            if Selection == "r":
                continue
            
            elif Selection == "a":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                interval = (dti - dtf) / NumPoints
                dtlist = [dti]
                for i in range(1,NumPoints + 1):
                    dtlist.append(dti - interval * i)
                NumValues = len(dtlist)

                f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8), sharex = "col", sharey = "row")  
                [i,N] = Dt_Difference(Euler,y0,v0,Cd,p0,A,t,g,m,h)
                if i < N:
                    continue
                else:
                    [i,N] = Dt_Difference(Modified_Euler,y0,v0,Cd,p0,A,t,g,m,h)
                    [i,N] = Dt_Difference(Runge_Kutta,y0,v0,Cd,p0,A,t,g,m,h)
                    plt.tight_layout()
                    f.suptitle("Convergence of the Functions with Changing $\Delta$t", fontsize = 14, y = 1.04)
                    plt.legend(["Euler","Modified Euler","Runge-Kutta"], bbox_to_anchor=(0, 2.4, 1, 0))
                    plt.show()

            elif Selection == "b":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                
            else:
                print(" ")
                print("This is not a valid choice")
        
# Section D

    elif Section_Input == "d":
        print(" ")
        print("You have chosen part (d)")
        
        Selection = "0"
        
        while Selection != "r":
        
            [speed,distance,time,v,y,i,k,N,t,dt] = Function_Run(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints,Section_Input,SectionG_Input)
        
            if speed[-1] - speed[-2] < 0.001:
                for i in range(N + 1):
                    if speed[i] >= 0.9 * speed[-1]:
                        print(" ")
                        print("The time taken for the velocity to reach 90%% that of terminal velocity was %.2f seconds" %(dt * i))
                        break
            else:
                print(" ")
                print("The time chosen was not long enough for terminal velocity to be reached and so 90 percent of this velocity could not be calculated")
                continue
            break
            
        Selection = "0"
    
# Section E
        
    elif Section_Input == "e":
        print(" ")
        print("You have chosen part (e)")
        
        f, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3,figsize = (15,12))
        figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9)
                
# Section G

    elif Section_Input == "f":     
        print(" ")
        print("You have chosen part (f)")

        Selection = "0"
        
        while Selection != "r":
            Selection = input("""Enter a choice:
    'a' (To plot the difference in the values),
    'b' (To plot the difference in the values on the same graph),
    'r' (To return to the previous menu): """)
            print(" ")
            print("You entered the choice:",Selection)
            
            SectionG_Input = "0"
        
            if Selection == "r":
                continue

             
            elif Selection == "a":
                f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3,figsize = (15,8))
                figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9)
                
            elif Selection == "b":
                f, (ax1, ax2) = plt.subplots(2, 1,figsize = (5,8))
                figure(y0,v0,Cd,p0,A,t,g,m,h,dt,Section_Input,ax1,ax1,ax1,ax2,ax2,ax2,ax3,ax3,ax3)
            
            else:
                print(" ")
                print("This is not a valid choice")
                continue
            
    elif Section_Input == "g":
        print(" ")
        print("You have chosen part (g)")
        
        Selection = "0"
        
        while Selection != "r":
            Selection = input("""Enter a choice:
    'a' (To plot the difference in the values against dt and N),
    'b' (To change the paramters of the plot),
    'r' (To return to the previous menu): """)
            print(" ")
            print("You entered the choice:",Selection)
            
            SectionG_Input = "0"
      
            if Selection == "r":
                continue
            
            elif Selection == "a":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                interval = (dti - dtf) / NumPoints
                dtlist = [dti]
                for i in range(1,NumPoints + 1):
                    dtlist.append(dti - interval * i)
                NumValues = len(dtlist)

                f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8))  
                [i,N] = Dt_Difference(Euler,y0,v0,Cd,p0,A,t,g,m,h)
                if i < N:
                    continue
                else:
                    [i,N] = Dt_Difference(Modified_Euler,y0,v0,Cd,p0,A,t,g,m,h)
                    [i,N] = Dt_Difference(Runge_Kutta,y0,v0,Cd,p0,A,t,g,m,h)
                    plt.tight_layout()
                    plt.show()
            

            elif Selection == "b":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                
            else:
                print(" ")
                print("This is not a valid choice")
                
    # Section F
        
    elif Section_Input == "h":
        print(" ")
        print("You have chosen part (h)")
        
        Selection = "0"
        
        while Selection != "r":
            Selection = input("""Enter a choice:
    'a' (To change Cd, A and m),
    'b' (To change v0, ρ0, g and h),
    'r' (To return to the previous menu): """)
            print(" ")
            print("You entered the choice:",Selection)
            
            if Selection == "r":
                continue
            
            elif Selection == "a":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                break
                
            elif Selection == "b":
                [y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints] = Inputs(y0,v0,Cd,p0,A,t,g,m,h,dt,dti,dtf,NumPoints)
                break
                
            else:
                print(" ")
                print("This is not a valid choice")
                           
    elif Section_Input ==  "q":
        print(" ")
        print("You have chosen to finish - goodbye.")
        plt.close()
      
    else:
        print(" ")
        print("This is not a valid choice")
           
Section_Input="0" 


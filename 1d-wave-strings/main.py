# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:09:40 2021

@author: Sorn
"""

import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def I(x, A, s, L):
    """I(x) is the initial condition, meaning t=0
    
        x is a variable in space
        A is the amplitude
        s is the intersection
        L is the length
        
        To form a "triangle-shaped" initial condition we
        return the value I(x) of the 1st linear function in the equation set for x less than s
        return the value I(x) of the 2nd linear function in the equation set for x larger than s
    """
    if x >= 0 and x <= s:
        return A*x/s
    if x >= s and x <= L:
        return A*(L-x)/(L-s)


def solver(A, s, L, T, c, dx, dt):
    """solver for:
        
        utt = (c**2)uxx
    
        A is the amplitude
        s is the intersection (also called x0 in some examples)
        L is the length of the string
        T is the total time steps
        c is the velocity
        
        returns
            u: a multidimensional list containing all u(x,t) in the mesh
            x: an equidistance list from 0 to L
            t: an equidistance list from 0 to T
    """
    Nx = int(round(L/dx)) # number of x mesh points
    Nt = int(round(T/dt)) # number of t mesh points
    
    x = np.linspace(0, L, Nx+1)
    t = np.linspace(0, T, Nt+1)
    
    dx = x[1] - x[0] # reset/fix dx
    dt = t[1] - t[0] # reset/fix dt
    
    # Courant's number
    C = c*(float(dt/dx))
    
    # Initialize multidimensional list
    u = np.zeros((Nt+1, Nx+1))
    
    # Set initial conditions for all x (when t=0)
    for i in range(0, Nx+1):
        u[0][i] = I(i*dx, A, s, L)
    
    # Apply initial function
    for i in range(1, Nx):
        u[1][i] = 0.5*(C**2)*(u[0][i+1]-2*u[0][i]+u[0][i-1])+u[0][i]

    # Apply central finite difference
    for n in range(1, Nt):
        for i in range(1, Nx):
            u[n+1][i] = (C**2)*(u[n][i+1]-2*u[n][i]+u[n][i-1])+2*u[n][i]-u[n-1][i]
        
    return u, x, t


def visualize(li, offset, T, dx, dt):
    """visualize creates an animated gif
    
        li is a multidimensional list containing the parameters for the solver
            [
                [A1, s1, L1, T1, c1, dx1, dt1, color1],
                [A2, s2, L2, T2, c2, dx2, dt2, color2],
                ...
                [AN, sN, LN, TN, cN, dxN, dtN, colorN],
            ]
            
        offset is the vertical spacing between the 1D waves, should be twice the amplitude
        
        T is the total number of time steps
    
        returns nothing
    """
    fig = plt.figure()
    plts = []
    
    # This list will be populated with u, x, and color
    solve_list = []
    
    # Pre-compute u and x values to save processing power
    for i in range(len(li)):
        u, x, t = solver(li[i][0], li[i][1], li[i][2], li[i][3], li[i][4], dx, dt)
        color = li[i][7]
        solve_list.append([u, x, color])
    
    # Group the correct animations together
    # for each time step n
    for n in range(T):
        plts_tmp = []
        
        # for each 1D wave in the list
        for i in range(len(li)):
            u, x, color = solve_list[i][0], solve_list[i][1], solve_list[i][2]
            p = plt.plot(x, u[n][:] + offset * i, color)
            plts_tmp.append(*p)
        
        plts.append(plts_tmp)
    
    # If PillowWriter does not work, try:
    # wr = animation.FFMpegFileWriter()
    # or another writer instead
    wr = animation.PillowWriter()
    ani = animation.ArtistAnimation(fig, plts) 

    # You must manually create an 'output/' directory, or change the filename to "waves.gif"
    ani.save("output/waves.gif", writer=wr)
    
    plt.show()


def main():
    # We currently have to set dx = dt, otherwise it won't plot
    dx = dt = 0.1
    
    # Total time steps
    T = 250
    
    # Length
    L = 5
    
    #       A    s   L  T   c    dx  dt color
    li = [[2.5, 0.2, L, T, 0.09, dx, dt, 'k'], # this is the bottom 1D wave in the plot
          [2.3, 1.0, L, T, 0.20, dx, dt, 'r'],
          [2.1, 2.0, L, T, 0.40, dx, dt, 'b'],
          [1.9, 3.0, L, T, 0.60, dx, dt, 'y'],
          [1.7, 4.0, L, T, 0.80, dx, dt, 'c'],
          [1.5, 4.8, L, T, 0.99, dx, dt, 'g']] # this is the top 1D wave in the plot
    
    # Spacing between the 1D waves in the plot. The offset should be twice the
    # largest amplitude such that the 1D waves don't overlap in the animation
    offset = 4
    
    visualize(li, offset, T, dx, dt)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:09:40 2021

@author: Sorn
"""

import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def I(x, A, s, L):
    """I(x) is the initial condition, meaning t=0"""
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
    """
    
    Nx = int(round((L-0)/dx)) # number of x mesh points
    Nt = int(round((T-0)/dt)) # number of t mesh points
    
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
    fig = plt.figure()
    plts = []
    
    solve_list = []
    
    # Pre-compute u and x values to save processing power
    for i in range(len(li)):
        u, x, t = solver(li[i][0], li[i][1], li[i][2], li[i][3], li[i][4], dx, dt)
        solve_list.append([u, x, li[i][7]])
    
    # Group the correct animations together
    for n in range(T):
        plts_tmp = []
        for i in range(len(li)):
            u, x, color = solve_list[i][0], solve_list[i][1], solve_list[i][2]
            p = plt.plot(x, u[n,0:] + offset * i, color)
            plts_tmp.append(*p)
        plts.append(plts_tmp)
        
    ani = animation.ArtistAnimation(fig, plts, interval=100)
    ani.save("output/waves" + ".gif")
    
    plt.show()


def main():
    dx = 0.1
    dt = 0.1
    
    T = 125
    L = 5
    
    li = [[2.5, 0.2, L, T, 0.3, dx, dt, 'k'],
          [2.3, 1.0, L, T, 0.4, dx, dt, 'r'],
          [2.1, 2.0, L, T, 0.5, dx, dt, 'b'],
          [1.9, 3.0, L, T, 0.6, dx, dt, 'y'],
          [1.7, 4.0, L, T, 0.7, dx, dt, 'c'],
          [1.5, 4.8, L, T, 0.8, dx, dt, 'g']]
    
    offset = 4
    
    visualize(li, offset, T, dx, dt)
    
if __name__ == "__main__":
    main()

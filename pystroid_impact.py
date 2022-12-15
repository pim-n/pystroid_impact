#!/bin/env python
# Copyright © 2022 Pim Nelissen.
# This software is licensed under the MIT license.
# Read more at https://mit-license.org/.

import numpy as np
from scipy import special
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

r0_x = 1.93
r0_y = 1.93
r_max = 0.3 # Impact radius of 3*10^2 km (2x radius of Chicxulub Crater in Mexico).
rlim = 0.5

u_0 = 100 # Initial temperature of the comet impact epicentre.

MAX_ITERATIONS = 50 # Sets the resolution and timeframe for simulation.
RESOLUTION = 1 # Integer scaling factor for resolution for x/y axes.

def u(x, y, t):
    """
    Function u(x,y,t) which determines the
    """
    X, Y = np.meshgrid(x, y)
    r = np.sqrt((X - r0_x)**2 + (Y - r0_y)**2)

    for i in range(len(x)):
        for j in range(len(y)):
            if X[i][j]**2 + Y[i][j]**2 <= 1:
                layer_temp = 55
                a = 1 # Hot iron has lower diffusivity than colder iron.
            elif 1 < X[i][j]**2 + Y[i][j]**2 <= 4:
                layer_temp = 40
                a = 2 # Slightly higher diffusivity for outer core.
            elif 4 < X[i][j]**2 + Y[i][j]**2 <= 6.5:
                layer_temp = 30
                a = 3 # diffusivity for mantle (metals).
            elif 6.5 < X[i][j]**2 + Y[i][j]**2 <= 7.5:
                layer_temp = 20
                a = 0.3 # stone has a lower diffusivity than most metals.
            elif 7.5 < X[i][j]**2 + Y[i][j]**2 <= 8:
                layer_temp = 0
                a = 2 # air has lower diffusivity than iron at 300K.
            else:
                layer_temp = -2.7
                a = 10000 # "infinite" diffusivity for outer space.

            u_0_exp = u_0**np.exp(-(t/10))

            r[i][j] = layer_temp + 0.5*u_0_exp*(special.erf((r_max - r[i][j])/np.sqrt(4*a*t)) - special.erf((-r_max-r[i][j])/np.sqrt(4*a*t)))

    return r

def plot_wave(xvals, yvals, t, i):
    wave = u(xvals, yvals, t[i])
    colors = ['black','darkblue','blue','yellow','orange','red','darkred']
    color_map = mcolors.LinearSegmentedColormap.from_list('mycmap', colors)

    plt.clf()
    plt.xlabel("x [10^6 m]")
    plt.ylabel("y [10^6 m]")
    plt.pcolor(xvals, yvals, wave, cmap=color_map, vmin = -2.7, vmax = 100)
    plt.gca().set_aspect('equal', 'box')
    plt.title(f"Comet impact t = {t[i]:.3f} units")
    return plt

def animate(i):
    plt = plot_wave(xrange, yrange, times, i)
    color_bar = plt.colorbar()
    color_bar.ax.yaxis.set_major_locator(MultipleLocator(4))
    color_bar.ax.tick_params(labelsize=8)
    color_bar.ax.set_title('T [10^2 °C]')

times = np.arange(0, MAX_ITERATIONS*10, 0.001)

xrange = np.linspace(0, 4, MAX_ITERATIONS*RESOLUTION)
yrange = np.linspace(0, 4, MAX_ITERATIONS*RESOLUTION)

anim = FuncAnimation(plt.figure(), animate, interval=1,
                     frames=MAX_ITERATIONS*10, repeat=False,
                     save_count=1000)

live = False

if live:
    plt.show()
else:
    anim.save("comet_simulation.gif", fps=10, writer='pillow')

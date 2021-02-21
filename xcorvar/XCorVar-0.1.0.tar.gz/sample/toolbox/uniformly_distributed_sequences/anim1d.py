'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import numpy as np
import itertools as it
import matplotlib.animation as animation
from matplotlib import pyplot as plt

from seq import RotTorSeq

dim = 4
sub_dim = 3
x = None

fig, ax = plt.subplots ()
line, = ax.plot([], [], color='black', linewidth=0, marker='.')
xdata, ydata = [], []

seq = RotTorSeq (dim, x)

def data_gen ():
    for _ in it.count ():
        yield seq.next ().space [sub_dim], 0

def init ():
    ax.set_ylim (-0.01, 0.01)
    ax.set_xlim (0, 1)
    del xdata [:]
    del ydata [:]
    line.set_data (xdata, ydata)
    return line,

def run (data):
    x, y = data
    xdata.append (x)
    ydata.append (y)
    line.set_data (xdata, ydata)
    return line,

anim = animation.FuncAnimation (fig, run, data_gen, interval=100, init_func=init)
plt.show ()
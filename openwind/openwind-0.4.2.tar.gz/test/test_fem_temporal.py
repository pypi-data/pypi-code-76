#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"


import sys
sys.path.append('..')
import itertools

import numpy as np
import numpy.fft
from numpy import exp, nan_to_num
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation, simulate
from openwind.technical.player import Player

temperature = 20.5
shape = [[0.0, 5e-3], [0.1, 5e-3], [0.2, 5e-3]]
# holes = []
holes = [[0.15, 0.03, 3e-3]]
l_ele = 0.04
order = 4

player = Player('IMPULSE_400us')


plt.figure()

for losses, nondim, spherical_waves in itertools.product([False, 'diffrepr8'], [False], [False, True]):
    print('*'*50)
    print("Performing simulation with losses =", losses,
          "; nondim =", nondim, "; spherical_waves =", spherical_waves)
    res = simulate(0.1, shape, holes, player=player,
                            l_ele=l_ele, order=order,
                            nondim=nondim, temperature=temperature,
                            losses=losses, radiation_category='planar_piston',
                            spherical_waves=spherical_waves,
                            verbosity=0)

    #%% Compute impedance from simu

    ts = res.ts
    p0, v0 = res.values['source_pressure'], res.values['source_flow']
    # Window the end of the impulse response to reduce artifacts
    window = np.hanning(len(p0))
    window[:len(p0)//2] = 1
    p0w, v0w = np.array(p0) * window, np.array(v0)*window

    p0_hat, v0_hat = numpy.fft.fft(p0w), numpy.fft.fft(v0w)

    Z = p0_hat / v0_hat
    fs_fft = numpy.fft.fftfreq(len(p0), ts[1]-ts[0])
    mask = (fs_fft > 20) * (fs_fft < 5000)

    Z = Z[mask]
    fs_fft = fs_fft[mask]


    #%% Compare with FEM

    fs = np.arange(20, 5000, 1)
    f_fem = ImpedanceComputation(fs, shape, holes,
                                   temperature=temperature, losses=losses,
                                   l_ele=l_ele, order=order,
                                   nondim=nondim,
                                   radiation_category='planar_piston',
                                   spherical_waves=spherical_waves,
                                   discontinuity_mass=False)


    #%% Compute error

    Z_fem = np.interp(fs_fft, fs, f_fem.impedance)
    err = sum(abs(np.log(abs(Z_fem)) - np.log(abs(Z))))/sum(abs(np.log(abs(Z_fem))))
    print("Relative error on log(abs(Z)) is :",err)

    lossy_or_lossless = "lossy" if losses else "lossless"
    lossy_or_lossless += " sph" if spherical_waves else " pla"
    dashed_if_lossless = '-' if losses else '--'

    #plt.figure()
    plt.semilogy(fs_fft, abs(Z_fem), 'r'+dashed_if_lossless, label="FEM, "+lossy_or_lossless)
    plt.semilogy(fs_fft, abs(Z), 'k'+dashed_if_lossless, label="Temporal, "+lossy_or_lossless)

    if not err < 1e-2:
        raise Exception("FEM and temporal simulation give very different results.")


plt.legend()
plt.show()

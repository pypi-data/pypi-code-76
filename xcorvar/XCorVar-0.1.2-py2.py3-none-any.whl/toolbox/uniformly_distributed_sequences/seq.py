'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import math as mth
import numpy as np
import copy as cpy

from matplotlib import pyplot as plt

primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
    307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
    401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
    701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
    907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
]

class State:

    #public:

        def __init__ (self, step, space):
            self.step = step
            self.space = space

        def __str__ (self):
            return 'step: ' + str (self.step) + ' space: ' + str (self.space) 

        def cpy (self):
            return State (self.step, cpy.copy (self.space))

class Seq:

    #public:

        def __init__ (self, state):
            self.state = state
            self.state_init = state.cpy ()
            self.hist = [state.cpy ()]

        @property
        def current (self):
            return self.state

        def restart (self):
            self.state = self.state_init.cpy ()
            self.hist = [self.state.cpy ()]

        def next (self, verbose=0):
            raise NotImplementedError

        def __call__ (self):
            return self.next ().space

        def not_end (self, n_max):
            return self.state.step < n_max

        def run (self, n_max, verbose=0):
            while self.not_end (n_max): self.next (verbose)
            return self

        def show (self):
            for state in self.hist: print (state)

        def plt_one_dim (self, dim):
            plt.figure ()
            plt.axis ([0, 1, 0, 0])
            plt.axhline (0, color='grey')
            for state in self.hist: plt.scatter (state.space [dim], 0, marker='.', color='black', lw=1)
            plt.show ()

        def plt_two_dim (self, dim1, dim2):
            plt.figure ()
            plt.axis ([0, 1, 0, 1])
            plt.axhline (0.5, color='grey')
            plt.axvline (0.5, color='grey')
            for state in self.hist: plt.scatter (state.space [dim1], state.space [dim2], marker='.', color='black', lw=1)
            plt.show ()

        def plt_three_dim (self, dim1, dim2, dim3):
            fig = plt.figure ()
            ax = fig.add_subplot (111, projection='3d')
            for state in self.hist: ax.scatter (state.space [dim1], state.space [dim2], state.space [dim3], color='black', marker='.')
            plt.show ()

class RotTorSeq (Seq):

    #public:

        def __init__ (self, dim, x=None):
            if x is None: x = np.zeros (dim)
            alpha = np.sqrt (primes [:dim])
            self.frac_alpha = np.vectorize (frac_part) (alpha)
            super ().__init__ (State (0, np.vectorize (frac_part) (x + alpha)))

        def next (self, verbose=0):
            self.state.step += 1
            self.state.space += np.array ([frac_alpha if frac_alpha + space < 1 else frac_alpha - 1 for space, frac_alpha in zip (self.state.space, self.frac_alpha)])
            self.hist.append (self.state.cpy ())
            if verbose > 0: print (self.state)
            return self.current

#mathkit:

def frac_part (x):
    p = 0
    while p+1 < x: p += 1
    return x-p

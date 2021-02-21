# coding: utf-8

import math as mth

class Step:

    #public:

        def __init__ (self, step):
            self.time = step
            self.brown = mth.sqrt (step)

class State:

    #public:

        def __init__ (self, time, space):
            self.time = time
            self.space = space

        def __str__ (self):
            return 'time: ' + str (self.time) + ' space: ' + str (self.space)

        def write (self, file):
            file.write (str (self.time) + ',' + str (self.space) + '\n')

        def get_attr (self):
            return self.time, self.space

class SuperState (State):

    #public:

        def __init__ (self, time, space):
            super ().__init__ (time, space)
            self.bar_space = space

        def __str__ (self):
            return super ().__str__ () + ' bar_space: ' + str (self.bar_space)

        def get_attr (self):
            return self.time, self.space, self.bar_space

class StoDifEq:

    #public:

        def __init__ (self, coeff):
            '''
            coeff: (time: float, space: float -> (b: float, sig: float))
            '''
            self.coeff = coeff

class MultiStoDifEq (StoDifEq):

    #public:

        def __init__ (self, coeff, corr=None):
            '''
            coeff: (time: float, space: float -> (b: float array, sig: float array))
            corr: float array array
            '''
            self.coeff = coeff
            if corr is not None: self.corr = corr

class MultiCorrDepStoDifEq (StoDifEq):

    #public:

        def __init__ (self, coeff):
            '''
            coeff: (time: float, space: float -> (b: float array, sig: float array, corr: float array array))
            '''
            self.coeff = coeff

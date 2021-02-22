#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Feb 25 10:51:51 CET 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: mcvariable.py -*-
# -*- purpose: -*-

'''
Class for MonteCarlo variable
'''

import random
import math

from typing import Union, Callable, Sequence, Generator

random.seed(None)

Number = Union[int, float]
ProbabilityLaw = Callable[..., Number]


# Below: defining two probability laws for general use

def law_gaussian(mean: Number = 0.0,
                 stddev: Number = 0.0) -> Number:
    'Returns a random value following a Gaussian probability law'
    return random.gauss(mean, stddev)


def law_flat(central: Number = 0.0,
             side: Number = 0.0) -> Number:
    'Returns a random value following a flat probability law'
    return random.uniform(central - side,
                          central + side)

def law_Gamma(center: Number = 0,
              stddev: Number = 1.0) -> Number:
    'Returns a random number following a laplace Law'
    beta = center / stddev ** 2.
    alpha = center / beta 
    return random.gammavariate(alpha, beta)

def law_triangular(center: Number = 0.0,
                   side: Number = 1.0,) -> Number:
    '''Returns a triangular distribution'''
    return random.triangular(center - side,
                             center + side,
                             center)

# Below: defining the class

class MCVariable():
    '''Monte Carlo variable'''

    def __init__(self,
                 parameters: Sequence[Number] = (0.0, 0.0),
                 law: ProbabilityLaw = law_gaussian,
                 keep_positive: bool = True,
                 non_zero: bool = True,
                 replace_zero_with: float = 1e-20):
        '''
        Initializes the variable

        - parameters (array of numbers) = (0, 0):
                              parameters of the probabilty law
        - law (function) =  law_gaussian : the probability law
        - keep_positive (bool) = True : keep the value >=0
        - non_zero (bool) = True : prevent the value to be eaxctly 0
        - replace_zero_with (float) = 1e-2: the value to replace 0 with
                                    (only if the previous parameter is True)
        '''
        self._parameters = parameters
        self._law = law
        self._keep_positive = keep_positive
        self._non_zero = non_zero
        self._replace_zero_with = replace_zero_with
        self.refresh()

    def refresh(self):
        '''create a new value from the probability law'''
        self.value = self._law(*self._parameters)
        if (self._keep_positive and
                self.value < 0):
            self.value = abs(self.value)
        if (self._non_zero and
                self.value == 0):
            self.value = self._replace_zero_with

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)


# Below: defining the generator

def MCGenerator(mcv: MCVariable,
                nmax: Number = math.inf,
                variable_type: type = float) -> Generator[Number, None, None]:
    '''Generator to produce many time the vairable value'''
    item_number = 0
    while item_number < nmax:
        mcv.refresh()
        yield variable_type(mcv)
        item_number += 1
# end of file

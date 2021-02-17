# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:34:59 2020

@author: danaukes
"""
import numpy
import pynamics

import logging
logger = logging.getLogger('pynamics.output')

class Output(object):
    def __init__(self,y_exp, system=None, constant_values = None,state_variables = None):
        import sympy
        system = system or pynamics.get_system()
        state_variables = state_variables or system.get_state_variables()
        constant_values = constant_values or system.constant_values
        self.y_expression = sympy.Matrix(y_exp)
        cons_s = list(constant_values.keys())
        self.cons_v = [constant_values[key] for key in cons_s]
        self.fy_expression = sympy.lambdify(state_variables+cons_s,self.y_expression)

    def calc(self,x):
        logger.info('calculating outputs')
        self.y = numpy.array([self.fy_expression(*(item.tolist()+self.cons_v)) for item in x]).squeeze()
        logger.info('done calculating outputs')
        return self.y

    def plot_time(self,t=None):
        import matplotlib.pyplot as plt
        plt.figure()
        try:
            self.y
        except AttributeError:
            self.calc()
        if t is None:
            plt.plot(self.y)
        else:
            plt.plot(t,self.y)


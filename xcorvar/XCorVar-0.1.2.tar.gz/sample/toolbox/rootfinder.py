'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

def dichotomy (function, left, right, target, precision, verbose=0):
    center = 0.5 * (left + right)
    value_center = function (center) - target
    stop_criterion = abs (value_center)
    if (stop_criterion < precision): return center
    value_left = function (left) - target
    value_right = function (right) - target
    if value_left * value_center < 0: return dichotomy (function, left, center, target, precision)
    elif value_center * value_right < 0: return dichotomy (function, center, right, target, precision)
    else: 
        if verbose > 0: 
            print ("Cannot find root with Dichotomy algorithm")
            print ("Left bound:", left, "left value:", value_left, "right bound:", right, "right value:", value_right)
        return None

def newton (function_derivative, target, initial_point, max_iterations=100, tolerance=1e-4, verbose=0):
    x = initial_point
    stop_criterion = 0
    iterations = 0
    while iterations < max_iterations and (stop_criterion > tolerance or iterations == 0):
        iterations += 1
        value_function, value_derivative = function_derivative (x)
        if value_derivative == 0: 
            if verbose > 0: print ('Zero division encountered')
            value_derivative = 1e-6
        difference = value_function - target
        x = x - difference / value_derivative
        stop_criterion = abs (difference)
    if stop_criterion < tolerance: return x
    else:
        if verbose > 0: 
            print ('Cannot find root with Newton algorithm')
            print ('Spread: ', stop_criterion)
        return None

def rootfinder (function, derivative, target, precision, guess, bounds, max_iterations=100, verbose=0):
    function_derivative = lambda x: (function (x), derivative (x))
    x = newton (function_derivative, target, guess, precision, max_iterations, verbose)
    if x != None: return x
    else:
        left, right = bounds
        x = dichotomy (function, left, right, target, precision, verbose)
        if x != None: return x
        else:
            if verbose > 0: print ('Cannot find root with rootfinder algorithm')
            return None
'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import numpy as np
from numpy.linalg import solve

from toolbox.random_variable import DEFAULT_RANDOM_NUMBER_GENERATOR
from toolbox.machine_learning.data_set import Data, DataSet, square_distance_between

class linearRegression:

    #public:

        def __init__ (self, data_set):
            self.data_set = data_set
            self.optimal_parameter = None

        def prediction (self, feature):
            return prediction (self.optimal_parameter, feature)

        def predictions (self, features):
            return predictions (self.optimal_parameter, features)

class LinearStandardRegression (linearRegression):

    #public:

        def __init__ (self, data_set):
            super ().__init__ (data_set)

        def find_optimal_parameter (self):
            self.optimal_parameter = find_optimal_parameter (self.data_set, 0)
        
class LinearRidgeRegression (linearRegression):

    #public:

        def __init__ (self, data_set):
            super ().__init__ (data_set)

        def find_optimal_parameter (self):
            self.optimal_parameter = find_optimal_parameter (self.data_set, self.optimal_coefficient) 

        def find_optimal_coefficient (self, coefficients, n_folds=3, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            sum_empirical_risk_errors = []
            folds = self.data_set.folds_split (n_folds, gen)
            for coefficient in coefficients:
                sum_empirical_risk_error = 0
                for fold in folds: 
                    data_validation = DataSet (fold)
                    data_train = DataSet ([data for data in self.data_set.data_list if data not in fold])
                    validation_features = [data.feature for data in data_validation.data_list]
                    validation_labels = [data.label for data in data_validation.data_list]
                    optimal_parameter = find_optimal_parameter (data_train, coefficient)
                    predicted_labels = predictions (optimal_parameter, validation_features)
                    empirical_risk_error = square_distance_between (predicted_labels, validation_labels)
                    sum_empirical_risk_error += empirical_risk_error
                sum_empirical_risk_errors.append ({'coefficient': coefficient, 'risk': sum_empirical_risk_error}) 
            min_sum_empirical_risk_errors = min (sum_empirical_risk_errors, key=lambda x: x ['risk'])
            self.optimal_coefficient = min_sum_empirical_risk_errors ['coefficient']

class LinearLassoRegression (linearRegression):

    #public:

        def __init__ (self, data_set):
            super ().__init__ (data_set)

        
        def find_optimal_parameter (self):
            self.optimal_parameter = find_optimal_parameter (self.data_set, self.optimal_coefficient) 

        def find_optimal_coefficient (self):
            pass

#toolkit:

def find_optimal_parameter (data_train, coefficient):
    d = data_train.features.shape [1]
    matrix = data_train.features.T @ data_train.features + coefficient * np.eye (d)
    vector = data_train.features.T @ data_train.labels
    optimal_parameter = solve (matrix, vector)
    return optimal_parameter

def prediction (optimal_parameter, feature):
    return np.dot (optimal_parameter, feature) 

def predictions (optimal_parameter, features):
    return features @ optimal_parameter 


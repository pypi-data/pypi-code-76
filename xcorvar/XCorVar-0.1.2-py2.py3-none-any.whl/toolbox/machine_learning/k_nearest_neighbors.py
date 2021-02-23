'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

from toolbox.machine_learning.data_set import Data, DataSet, square_distance_between
from toolbox.random_variable import DEFAULT_RANDOM_NUMBER_GENERATOR, Choices

class NearestNeighbors:

    #public:

        def __init__ (self, data_set): 
            self.data_set = data_set

        def find_optimal_parameter (self, number_of_neighbors, rate=2/3, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            data_set_train, data_set_validation = self.data_set.train_validation_split (rate, gen)
            features_validation = [data.feature for data in data_set_validation.data_list]
            labels_validation = [data.label for data in data_set_validation.data_list]
            empirical_risk_errors = []
            for k in number_of_neighbors:
                labels_predicted = predictions (data_set_train, features_validation, k)
                empirical_risk_error = square_distance_between (labels_predicted, labels_validation)
                empirical_risk_errors.append ({'n_neighbors': k, 'risk': empirical_risk_error})
            min_empirical_risk_errors = min (empirical_risk_errors, key=lambda x: x ['risk'])
            self.optimal_parameter = min_empirical_risk_errors ['n_neighbors']

        def prediction (self, feature):
            return prediction (self.data_set, feature, self.optimal_parameter)    

        def predictions (self, features, number_of_neighbors):
            return [self.prediction (feature) for feature in features]        

#toolkit:

def prediction (train, feature, number_of_neighbors):
    labels_distances = train.get_nearest_neighbors (feature, number_of_neighbors)
    return average (labels_distances, number_of_neighbors)

def predictions (train, features, number_of_neighbors):
    return [prediction (train, feature, number_of_neighbors) for feature in features]

#mathkit:

def argmax (labels_distances):
    labels = [label for label, _ in labels_distances]
    return max (set (labels), key=labels.count)

def average (labels_distances, number_of_neighbors):
    return sum ([label for label, _ in labels_distances]) / number_of_neighbors
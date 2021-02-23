'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import numpy as np

from toolbox.random_variable import DEFAULT_RANDOM_NUMBER_GENERATOR, Choices, Folds

class Data:

    #public:

        def __init__ (self, feature, label): 
            self.feature = feature
            self.label = label

        def __str__ (self):
            return 'feature: ' + str (self.feature) + 'label: ' + str (self.label)

class DataSet:

    #public:

        def __init__ (self, data_list): 
            self.data_list = data_list
            self.n_data = len (data_list)

        @property
        def features (self):
            return np.array ([data.feature for data in self.data_list])

        @property
        def labels (self):
            return np.array ([data.label for data in self.data_list])

        def show (self):
            for data in self.data_list: 
                print (data)
        
        def train_validation_split (self, rate=1/3, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            n_validation = int (rate * self.n_data)
            data_validation = Choices (n_validation, self.data_list) (gen)
            data_train = [data for data in self.data_list if data not in data_validation] 
            return DataSet (data_train), DataSet (data_validation)

        def folds_split (self, n_folds, gen=DEFAULT_RANDOM_NUMBER_GENERATOR):
            return Folds (n_folds, self.data_list) (gen)

        def get_nearest_neighbors (self, feature, number_of_neighbors): 
            distances = [{'index': index, 'distance': square_distance_between (feature, data.feature)} for index, data in enumerate (self.data_list)]
            distances.sort (key=lambda x: x ['distance'])
            return [self.data_list [distance ['index']].label for distance in distances [:number_of_neighbors]]

#mathkit:

def square_distance_between (X1, X2):
    return sum ([(x1 - x2) ** 2 for x1, x2 in zip (X1, X2)])
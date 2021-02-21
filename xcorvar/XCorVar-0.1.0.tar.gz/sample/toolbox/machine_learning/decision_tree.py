'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/python3
# coding: utf-8

import numpy as np

class Node:

    #public:

        def __init__ (self, indexes, variable, threshold, impurity=0, children=[]):
            self.indexes = indexes
            self.impurity = impurity
            self.variable = variable
            self.threshold = threshold
            self.children = children
        
        def show (self):
            print ('Impurity: ', self.impurity)
            print ('Variable: ', self.variable)
            print ('Threshold: ', self.threshold)
            for child in self.children: child.show ()
                
class Tree:

    #public:

        def __init__ (self, data_set):
            self.features = data_set.features
            self.labels = data_set.labels
            self.n_variables = len (data_set.data_list [0].feature)
    
        def build (self, node):
            max_impurity = 0
            for index_variable in range (self.n_variables):
                features = [self.features [index] [index_variable] for index in node.indexes]
                thresholds = get_thresholds (features)
                for threshold in thresholds:
                    indexes_left = [index for index in node.indexes if self.features [index] [index_variable] < threshold]
                    indexes_right = [index for index in node.indexes if self.features [index] [index_variable] > threshold]
                    impurity_left = get_impurity ([self.labels [index] for index in indexes_left])
                    impurity_right = get_impurity ([self.labels [index] for index in indexes_right])
                    total_impurity = impurity_left + impurity_right
                    if total_impurity > max_impurity: 
                        max_impurity = total_impurity
                        node_left = Node (indexes_left, impurity_left, index_variable, threshold)
                        node_right = Node (indexes_right, impurity_right, index_variable, threshold)
            node.children = [node_left, node_right]
            self.build (node_left)
            self.build (node_right)

#tookit:

def get_thresholds (features):
    
    return []
    
def get_impurity (labels):
    return np.var (labels)


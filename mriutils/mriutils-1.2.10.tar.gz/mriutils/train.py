#!/usr/bin/env python

from sklearn.model_selection import train_test_split
import os
import numpy as np
from utils.norm import Normalization


class Train:
    def __init__(self, model, training, channels, n_classes):
        self.model = model
        self.training = training
        self.lens = len(training)
        self.channels = channels
        self.n_classes = n_classes

    def data_split(self, X_train, Y_train, test_ratio = 0.3):
        train, test = train_test_split(X_train, Y_train, test_size = test_ratio, random_state = 1024)
        return train, test

    def train(self, data_mode, label_mode, epochs = 1000, batch_size = 2, save_name = None):
        save_name = 'tmp.hdf5' if save_name == None else save_name
        if os.path.exists(save_name):
            self.model.load_weights(save_name) 
        X_train = np.resize(self.training[data_mode], (self.lens, self.training[data_mode][0].shape[0], self.training[data_mode][0].shape[1], self.training[data_mode][0].shape[2], self.channels))
        Y_train = np.resize(self.training[label_mode], (self.lens, self.training[label_mode][0].shape[0], self.training[label_mode][0].shape[1], self.training[label_mode][0].shape[2]))
        X_train = Normalization(X_train, 'data').norm()
        Y_train = Normalization(Y_train, 'label', self.n_classes).norm()
        train, test = self.data_split(X_train, Y_train)
        self.model.fit(X_train[train], Y_train[train], validation_data = (X_train[test], Y_train[test]), epochs = epochs, batch_size = batch_size)
        self.model.save_weights("%s" %(save_name), True)
        
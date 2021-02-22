#!/usr/bin/env python

import os
import numpy as np
from utils.norm import Normalization


class Test:
    def __init__(self, model, save_name, channels, n_classes, testing):
        self.model = model
        self.save_name = save_name
        self.channels = channels
        self.n_classes = n_classes
        self.testing = testing
        self.lens = len(testing)

    def test(self, data_mode, label_mode, save_path, measure = False, metrics = None):
        if os.path.exists(self.save_name):
            self.model.load_weights(self.save_name)  
        else:
            print('Model not exist!')
            return None
        x_test = np.resize(self.testing[data_mode], (self.lens, self.testing[data_mode][0].shape[0], self.testing[data_mode][0].shape[1], self.testing[data_mode][0].shape[2], self.channels))
        y_test = np.resize(self.testing[label_mode], (self.lens,self.testing[label_mode][0].shape[0], self.testing[label_mode][0].shape[1], self.testing[label_mode][0].shape[2]))
        x_test = Normalization(x_test, 'data').norm()
        num = len(x_test)
        ret = []
        for i in range(num):
            pred = self.model.predict(np.resize(x_test[i], (1, x_test[0].shape[0], x_test[0].shape[1], x_test[0].shape[2], x_test[0].shape[3])))
            pred = Normalization(pred, 'pred', self.n_classes).norm()
            np.save(os.path.join(save_path, str(i) + '_pred.npy'), pred)
            if measure:
                tmp_ret = []
                for item in metrics:
                    y_test_ = Normalization(y_test[i], 'test').norm()
                    tmp_ret.append(item(y_test_, pred))
                ret.append(tmp_ret)
        return ret


        
        
        
    
        
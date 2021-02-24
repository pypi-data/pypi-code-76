# %%
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
from tensorflow import keras

import copy


# %%
class data_management:
            
    @staticmethod
    def get_subset(X, y=None):
        subset = type("xClass", (object,), {})
        subset.dfX = pd.DataFrame(X)
        
        if(str(type(y)) != str(type(None)) and len(set(y)) == 1):
            y = None
        
        subset.y = y
        subset.y_enc = None
        subset.y_ohe = None
        
        return subset
        
    @staticmethod
    def n_subset_split(X, y, ratios, random_state):
        ratios = np.array(ratios)
        
        if(len(ratios) == 0):
            return ([X,y],)
        
        if(str(type(y)) == str(type(None)) or len(set(y)) == 1):
            x1, x2 = train_test_split(X, test_size=sum(ratios), random_state=random_state)
            y1 = y2 = None
        else:
            x1, x2, y1, y2 = train_test_split(X, y, stratify=y, test_size=sum(ratios), random_state=random_state)
            
        ratios = (ratios / sum(ratios))[1:]
        rest = data_management.n_subset_split(x2, y2, ratios, random_state)
        
        return ([x1,y1], *rest)
        
    def train_val_test_split(self, dataset, random_state=42):
        # dataset = [[], 0.0, 0.2, 0.2]
        # dataset = [[], 0.0, 0.2, []]
        # dataset = [[], 0.4, 0, 0]

        #####################################################
        assert len(dataset) == 4
        #####################################################
        assert str(type(dataset[0])) == str(type(list()))
        #####################################################
        ratiosum = 0.0
        for ratio in dataset:
            if(str(type(ratio)) != str(type(list()))):
                assert ratio < 1.0 and ratio >= 0.0
                ratiosum += ratio
        assert ratiosum < 1.0 and ratiosum >= 0.0
        #####################################################
        for subset in dataset:
            if(str(type(subset)) == str(type(list())) and len(subset) == 1):
                # subset.append([0]*len(subset[0]))
                subset.append(None)
        #####################################################
        for subset in dataset:
            if(str(type(subset)) == str(type(list()))):
                subset[0] = pd.DataFrame(subset[0])
        #####################################################
        #####################################################
        ratios = []
        for ratio in dataset:
            if(str(type(ratio)) != str(type(list())) and ratio != 0):
                ratios.append(ratio)
        #####################################################
        #####################################################
        
        splittedsubsets = self.n_subset_split(*dataset[0], ratios, random_state)
        
        trainsubset = splittedsubsets[0]
        splittedsubsets = splittedsubsets[1:]
        dataset = dataset[1:]
        
        othersubsets = []
        for subset in dataset:
            if(str(type(subset)) == str(type(list())) ):
                othersubsets.append(subset)
            elif(subset == 0):
                othersubsets.append(None)
            else:
                othersubsets.append(splittedsubsets[0])
                splittedsubsets = splittedsubsets[1:]
                
        self.train = self.get_subset(*trainsubset)
        self.pre = self.get_subset(*othersubsets[0]) if othersubsets[0] else othersubsets[0]
        self.valid = self.get_subset(*othersubsets[1]) if othersubsets[1] else othersubsets[1]
        self.test = self.get_subset(*othersubsets[2]) if othersubsets[2] else othersubsets[2]
        self.labelencoder = None
        
    def encode_labels(self, labelencoder=None):
        assert str(type(self.train.y)) != str(type(None))
        
        if(labelencoder == None):
            if(self.labelencoder != None):
                pass
            else:
                labelencoder = LabelEncoder()
                labelencoder.fit(self.train.y)
                self.labelencoder = labelencoder
                
        else:
            self.labelencoder = labelencoder
            
        label_count = len(self.labelencoder.classes_)
        
        self.apply_func_f2f( lambda y : self.labelencoder.transform(y), "y", "y_enc")
        self.apply_func_f2f( lambda y_enc : keras.utils.to_categorical(y_enc, num_classes=label_count), "y_enc", "y_ohe")


# %%
class DatasetContainer(data_management):
    
    def __init__(self, dataset, random_state=42):
        
        self.train_val_test_split(dataset,random_state)
        
    ###################################################
    
    def apply_func_f2f(self, func1, sourcefield, targetfield):
        setattr(self.train, targetfield, func1(getattr(self.train, sourcefield)))
        if(self.pre):
            setattr(self.pre, targetfield, func1(getattr(self.pre, sourcefield)))
        if(self.valid):
            setattr(self.valid, targetfield, func1(getattr(self.valid, sourcefield)))
        if(self.test):
            setattr(self.test, targetfield, func1(getattr(self.test, sourcefield)))
            
    def apply_func_all(self, func1):
        self.train = func1(self.train)
        if(self.pre):
            self.pre = func1(self.pre)
        if(self.valid):
            self.valid = func1(self.valid)
        if(self.test):
            self.test = func1(self.test)
            
    ###################################################
    
    def copy(self):
        return copy.deepcopy(self)


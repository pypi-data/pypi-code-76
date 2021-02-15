'''
#########################################################
# SCI-KIT-MCDA Library                                  #
# Author: Antonio Horta                                 #
# https://gitlab.com/cybercrafter/scikit-mcda           #
# Cybercrafter ® 2021                                   #
#########################################################
'''

import pandas as pd
import numpy as np
import copy
from tabulate import tabulate
from .constants import *
import math

class MCDA:
    """
    Class: MCDA: Multi-Criteria Decision Aid
    """
    def __init__(self):
        self.df_original = 0
        self.weights = []
        self.signals = []
        self.normalization_method = None
        self.df_normalized = 0
        self.df_weighted = 0
        self.df_decision = []

    def dataframe(self, alt_data, alt_labels=None, criteria_labels=None):
        """
        Set data for MCDM problem and save it into attribute: df_original.
        
        :param alt_data: They are the values of each criteria (columns) for each alternative (rows),
        :type alt_data: list of list
        
        :param alt_labels: (Optional) Requires a list of labels for alternatives. If not provided, labels are automatically defined,
        :type alt_labels: list
        
        :param criteria_labels: (Optional) Requires a list of labels for criteria. If not provided, labels are automatically defined. Its very important that order of criteria are from less to more important due to some algorithms requirements for weights definition.
        :type criteria_labels: list
        
        :returns: no value
        :rtype: none
        """

        # define criteria labels if not exists
        if criteria_labels is None:
            criteria_labels = []
            for s in range(1, len(alt_data[0])+1):
                criteria_labels.append("C" + str(s))

        # define alternative labels if not exists
        if alt_labels is None:
            alt_labels = []
            for a in range(1, len(alt_data)+1):
                alt_labels.append("A" + str(a))

        

        df_data = pd.DataFrame(data=alt_data, columns=criteria_labels)
        df_data.insert(loc=0,
                    column='alternatives',
                    value=alt_labels)
        dfo = df_data

        self.df_original = copy.copy(dfo)
        self.df_calc = copy.copy(dfo)
        self.decision = []

    def set_weights_manually(self, weights, free=False):
        """
        Set data weights manually for MCDM problems and save it into attribute: weights.
        
        :param weights: The numeric values of weights for each criteria (columns),
        :type weights: list
        
        :param free: (default=False) If False, checks if weight value is a float between 0 and 1 and the sum is 100%,
        :type free: boolean
        
        :returns: no value
        :rtype: none
        """
        if self.__check_weights(weights, free) is True:
            self.weights = weights
        else:
            raise ValueError("Invalid weights! Each weight must be float between 0 and 1 and same number of criteria")

    def set_weights_by_ranking_A(self):
        """
        Set weights for MCDM problems and save it into attribute: weights.
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / rj} / {∑[1 / rk], where k range is 1 to n}

        :returns: no value
        :rtype: none
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[1 / rk]
            b = b + (1 / k)
        for j in r: # Wj = {1 / rj} / b
            W.append((1 / j) / b)
        
        self.weights = W

    def set_weights_by_ranking_B(self):
        """
        Set weights for MCDM problems and save it into attribute: weights.
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1} / {∑[ n - rk + 1], where k range is 1 to n}

        :returns: no value
        :rtype: none
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + (n - k + 1)
        for j in r: # Wj = {n -rj + 1} / b
            W.append((n - j + 1) / b)
        
        self.weights = W

    def set_weights_by_ranking_C(self):
        """
        Set weights for MCDM problems and save it into attribute: weights.
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / n} * {∑[ 1 / K ], where K range is j to n}

        :returns: no value
        :rtype: none
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1)
        r = r[::-1].tolist()

        W = []
        b = 0
        a = 1 / n
        for k in r: # b = ∑[ 1 / K ]
            b = b + (1 / k)
            W.insert(0, a * b)
        
        self.weights = W

    def set_weights_by_ranking_B_POW(self, P=0):
        """
        Set weights for MCDM problems and save it into attribute: weights.
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1}^P / {∑[ n - rk + 1]^P, where k range is 1 to n}
        
        :param P: (default=0) 0 results in the same weight for all criteria,
        :type P: int

        :returns: no value
        :rtype: none
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + pow((n - k + 1),P)
        for j in r: # Wj = {n -rj + 1} / b
            W.append(pow((n - j + 1), P) / b)
  
        self.weights = W

    def set_weights_by_entropy(self, normalization_method_for_entropy=LinearSum_):
        """
        Set weights by entropy for MCDM problems and save it into attribute: weights.
        IMPORTANT: signals must have to be set before weights

        :param normalization_method_for_entropy: (default=LinearSum_) 0 results in the same weight for all criteria,
        :type normalization_method_for_entropy: some value defined in NORMALIZATION_METHODS constant

        :returns: no value
        :rtype: none
        """

        # check if signal are defined before weigths by entropy.   They are required for normalization
        if self.signals == []:
            raise ReferenceError("Signals must have to be set before weights to use entropy")

        # Save current norm method
        current_norm_method = self.normalization_method

        # appy new norm method for entropy and apply
        self.__set_normalization_method(normalization_method_for_entropy)

        self.__normalize()
        x, y = self.df_normalized.iloc[:,1:].shape

        h = 1 / math.log(x)

        entropies = -h * (self.df_normalized.iloc[:, 1:] * np.log(self.df_normalized.iloc[:, 1:])).sum(axis=0)

        distances = pd.DataFrame(1 - entropies)
        distances_sum = distances.iloc[:,:].sum(axis=0)

        # Weights vector
        W = distances/distances_sum.values

        w = []
        for i in W.values.tolist():
            w.append(i[0])
        
        # set entropy weights
        self.weights = w

        #back current nor method
        self.normalization_method = current_norm_method

    def set_weights_by_AHP(self, saaty_preference_matrix):
        """
        Set weights by AHP for MCDM problems and save it into attribute: weights.

        e.g.
                                              # C1   C2     C3   C4 
        w_AHP = electre_i.set_weights_by_AHP([[  1,    4,    5,   7],   # C1
                                              [1/4,    1,    3,   5],   # C2
                                              [1/5,  1/3,    1,   3],   # C3
                                              [1/7,  1/5,  1/3,   1]])  # C4
    
        :param saaty_preference_matrix: matrix of preferences of values in Saaty scale.
        :type saaty_preference_matrix: list

        :returns: no value
        :rtype: none
        """
        if self.__check_AHP_matrix(saaty_preference_matrix) is True:  
            saaty_preference_matrix = pd.DataFrame(saaty_preference_matrix)
            priority_vector = (saaty_preference_matrix / saaty_preference_matrix.sum(axis=0)).mean(axis=1)
            sum_of_weights = (saaty_preference_matrix * priority_vector).sum(axis=1)    
            lambda_max = (sum_of_weights/priority_vector).mean()
            n = len(priority_vector)
            CI = (lambda_max - n)/(n -1) 
            CR = CI/SAATY_RI[n-1]
        if CR <= 0.1:
            self.weights = priority_vector.values.tolist()
            return {"consistency": True, "lambda": lambda_max, "CIndex": CI, "CRatio": CR}
        else:
            return {"consistency": False, "lambda": lambda_max, "CIndex": CI, "CRatio": CR}
                  
    def set_signals(self, signals):
        """
        Set the target function of criteria for maximization or minimization and save it into attribute: signals.

        e.g.
            set_signals([-1, 1, 1, 1, 1])

            or using contants MIN and MAX
            
            set_signals([MIN, MAX, MAX, MAX, MAX])

        :param signals: 1 or MAX for maximization or MIN, -1 for minimization.
        :type signals: list

        :returns: no value
        :rtype: none
        """
        if self.__check_signals(signals) is True:
            self.signals = signals
        else:
            raise ValueError("Invalid signals! It's must be a list of 1 or -1")

    def __set_normalization_method(self, normalization_method):
        if normalization_method in NORMALIZATION_METHODS:
            self.normalization_method = normalization_method 
        elif normalization_method is None:
            self.normalization_method == None
        else:
            raise ValueError("Invalid parameter! Use a method defined in constants. e.g. normalization_D, zScore etc...")

    def __normalize(self, ignore_signals=False):
        if self.normalization_method == Vector_:
            self.__norm_Vector(ignore_signals)
        elif self.normalization_method == LinearSum_:
            self.__norm_LinearSum(ignore_signals)
        elif self.normalization_method == LinearMinMax_:
            self.__norm_LinearMinMax(ignore_signals)
        elif self.normalization_method == LinearMax_:
            self.__norm_LinearMax(ignore_signals)
        elif self.normalization_method == EnhancedAccuracy_:
            self.__norm_EnhancedAccuracy(ignore_signals)
        elif self.normalization_method == Logarithmic_:
            self.__norm_Logarithmic(ignore_signals)
        else:
            self.df_normalized = self.df_original

    def __norm_ZScore(self, ignore_signals=False):
        normalized = (self.df_original.iloc[:, 1:] - self.df_original.iloc[:, 1:].mean(axis=0))/self.df_original.iloc[:, 1:].std(axis=0)
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)
               
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_EnhancedAccuracy(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = 1 - (self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:])/((self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:]).sum(axis=0))
        # _min for minimizing 
        normalized_min = 1 - (self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0))/((self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0)).sum(axis=0))
       
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_Logarithmic(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = np.log2(self.df_original.iloc[:, 1:]) / np.log2( np.log2(self.df_original.iloc[:, 1:]).prod(axis = 0) * self.df_original.iloc[:, 1:] )
        # _min for minimizing 
        normalized_min = 1 - ( (1 - normalized_max) / ( normalized_max.shape[0] - 1) )
          
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearMax(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = (self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].max(axis=0))
        # _min for minimizing 
        normalized_min = (self.df_original.iloc[:, 1:].min(axis=0)/self.df_original.iloc[:, 1:])
               
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearMinMax(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = (self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0))/(self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:].min(axis=0))
        # _min for minimizing 
        normalized_min = (self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:])/(self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:].min(axis=0))
               
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_LinearSum(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].sum(axis=0)
        # _min for minimizing 
        normalized_min = (1/self.df_original.iloc[:, 1:])/(1/self.df_original.iloc[:, 1:]).sum(axis=0)
        
       
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized

    def __norm_Vector(self, ignore_signals=False):
        # _max for maximizing 
        normalized_max = self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
        # _min for minimizing 
        normalized_min = 1 - self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
       
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        if ignore_signals is True:
            normalized = normalized.join(normalized_max.iloc[:, :])
        else:
            i = 0
            for s in self.signals:
                if s == 1:
                    normalized = normalized.join(normalized_max.iloc[:, i])
                else:
                    normalized = normalized.join(normalized_min.iloc[:, i])
                i = i + 1
        
        self.df_normalized = normalized


        # _max for maximizing 
        normalized_topsis = self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
        
        # make nomalized matrix based in signals
        normalized = pd.DataFrame(self.df_original.iloc[:, 0])
        normalized = normalized.join(normalized_topsis.iloc[:, :])
        
        self.df_normalized = normalized

    def __weighting_from_normalized(self):
        weighted = self.df_normalized.iloc[:, 1:] * self.weights
        self.df_weighted = pd.DataFrame(self.df_original.iloc[:,0]).join(weighted)

    def __check_weights(self, weights, free=False):
        result = False
        if type(weights) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(weights) \
               and ((all(isinstance(n, float) for n in weights) \
               and all((n >= 0 and n <= 1) for n in weights) \
               and round(sum(weights)) == 1) \
               or (free is True)):
                result = True
        return result

    def __check_signals(self, signals):
        result = False
        if type(signals) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(signals) \
               and all(isinstance(n, int) for n in signals) \
               and all((n == 1 or n == -1) for n in signals):                
                result = True
        return result

    def __check_AHP_matrix(self, saaty_preference_matrix):
        if type(saaty_preference_matrix) == list:  
            saaty_preference_matrix = pd.DataFrame(saaty_preference_matrix)
            x, y = saaty_preference_matrix.shape 
            # n = len(self.df_original.columns.values) -1
            if False in saaty_preference_matrix.iloc[:, :].isin(SAATY_SCALE).values or x != y:
                raise ValueError("Value not in Saaty Scale or wrong dimentions in matrix")
            else:
                for i in range(x):
                    for j in range(y):
                        if saaty_preference_matrix.iloc[i, j] == 1/saaty_preference_matrix.iloc[j, i] \
                           or saaty_preference_matrix.iloc[j, i] == 1/saaty_preference_matrix.iloc[i, j] \
                           or (saaty_preference_matrix.iloc[j, i] == 1 and i == j): 
                            pass
                        else:
                            raise ValueError("Incoherent values of preferences", saaty_preference_matrix.iloc[i, j], )
        return True

    def pretty_original(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """
        return tabulate(self.df_original, headers='keys', tablefmt=tablefmt)

    def pretty_normalized(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """
        return tabulate(self.df_normalized, headers='keys', tablefmt=tablefmt)

    def pretty_weighted(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """        
        return tabulate(self.df_weighted, headers='keys', tablefmt=tablefmt)

    def pretty_decision(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """
        return tabulate(self.df_decision, headers='keys', tablefmt=tablefmt)
        


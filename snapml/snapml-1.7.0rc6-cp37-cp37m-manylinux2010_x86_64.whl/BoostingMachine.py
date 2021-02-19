# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np
import sys
import math
import warnings

from snapml.utils import _is_mpi_enabled, _param_check
_mpi_enabled = _is_mpi_enabled()

if sys.version_info[0] < 3:
    import libsnapmllocal2 as libsnapml
else:
    import snapml.libsnapmllocal3 as libsnapml

class BoostingMachine:

    """
    BoostingMachine

    This class implements a boosting machine that can be used to construct an ensemble of decision trees.
    It can be used for both clasification and regression tasks.
    In constrast to other boosting frameworks, Snap ML's boosting machine dose not utilize a fixed maximal tree depth at each boosting iteration.
    Instead, the tree depth is sampled at each boosting iteration according to a discrete uniform distribution.
    The fit and predict functions accept numpy.ndarray data structures.

    Boosting params dictionary has the following structure:

    params = {
        'boosting_params' {
            'num_round': 10,
            'objective': 'mse',
            'random_state': 0,
            'colsample_bytree': 1.0,
            'subsample': 1.0,
            'verbose': False,
            'lambda_l2': 0.0,
            'early_stopping_rounds': 10,
            'compress_trees': False,
            'base_score': None
        },
        'tree_params': {
            'min_max_depth: 1,
            'max_max_depth: 6,
            'num_threads': 1,
            'use_histograms': True,
            'hist_nbins': 256,
            'use_gpu': False,
            'gpu_id': 0,
            'select_probability': 1.0
        },
        'kernel_params': {
            'gamma': 1.0,
            'n_components': 10,
            'num_threads': 1,
        },
        'ridge_params': {
            'regularizer': 1.0,
            'num_threads': 1,
            'fit_intercept': False
        }
    }

    For classification set 'objective' to 'logloss', and for regression use 'mse'.

    Parameters
    ----------

    params: dict

    Attributes
    ----------

    """
    PARAMS = {
        "boosting_params": [
            {"name": "num_round", "attr": [{"type": "int", "ge": 1}]},
            {"name": "objective", "attr": [{"values":["mse", "logloss", "cross_entropy"]}]},
            {"name": "learning_rate", "attr": [{"type": "float", "ge": 0}]},
            {"name": "random_state", "attr": [{"type": "int"}]},
            {"name": "colsample_bytree", "attr": [{"type": "float", "gt": 0, "le": 1}]},
            {"name": "subsample", "attr": [{"type": "float", "gt": 0, "le": 1}]},
            {"name": "verbose", "attr": [{"type": "bool"}]},
            {"name": "enable_profile", "attr": [{"type": "bool"}]},
            {"name": "lambda_l2", "attr": [{"type": "float", "ge": 0}]},
            {"name": "early_stopping_rounds", "attr": [{"type": "int", "ge": 1}]},
            {"name": "compress_trees", "attr": [{"type": "bool"}]},
            {"name": "base_score", "attr": [{"values": [None]},{"type": "float"}]}],
        "tree_params": [
            {"name": "min_max_depth", "attr": [{"type": "int", "ge": 1}]},
            {"name": "max_max_depth", "attr": [{"type": "int", "ge": 1}]},
            {"name": "num_threads", "attr": [{"type": "int", "ge": 1}]},
            {"name": "use_histograms", "attr": [{"type": "bool"}]},
            {"name": "hist_nbins", "attr": [{"type": "int", "gt": 0, "le": 256}]},
            {"name": "use_gpu", "attr": [{"type": "bool"}]},
            {"name": "gpu_id", "attr": [{"type": "int", "ge": 0}]},
            {"name": "parallel_by_example", "attr": [{"type": "bool"}]},
            {"name": "select_probability", "attr": [{"type": "float", "ge": 0, "le": 1}]}],
        "ridge_params": [
            {"name": "regularizer", "attr": [{"type": "float", "gt": 0}]},
            {"name": "num_threads", "attr": [{"type": "int", "ge": 1}]},
            {"name": "fit_intercept", "attr": [{"type": "bool"}]},
            {"name": "select_probability", "attr": [{"type": "float", "ge": 0, "le": 1}]}],
        "kernel_params": [
            {"name": "gamma", "attr": [{"type": "float"}]},
            {"name": "n_components", "attr": [{"type": "int", "ge": 1}]},
            {"name": "num_threads", "attr": [{"type": "int", "ge": 1}]}]
    }

    def __init__(self,  params=None):

        self.ptr_ = np.array([], dtype=np.uint64)

        # params is a dictionary of dictionaries that includes all the model parameters 
        # params = {boosting_params, tree_params, rbf_params, ridge_params}
        # all *_params are dictionaries
        self.params_ = {}
        self.boosting_params_ = {}
        self.tree_params_ = {}
        self.kernel_params_ = {}
        self.ridge_params_ = {}
        
        # define boosting model defaults
        self.boosting_params_['num_round'] = 10
        self.boosting_params_['objective'] = 'mse'
        self.boosting_params_['learning_rate'] = 0.1
        self.boosting_params_['random_state'] = 0
        self.boosting_params_['colsample_bytree'] = 1.0
        self.boosting_params_['subsample'] = 1.0
        self.boosting_params_['verbose'] = False
        self.boosting_params_['enable_profile'] = False
        self.boosting_params_['lambda_l2'] = 0.0
        self.boosting_params_['early_stopping_rounds'] = 10
        self.boosting_params_['compress_trees'] = False
        self.boosting_params_['base_score'] = None
        self.params_['boosting_params'] = self.boosting_params_
        
        # define tree model defaults
        self.tree_params_['min_max_depth'] = 1
        self.tree_params_['max_max_depth'] = 6
        self.tree_params_['num_threads'] = 1
        self.tree_params_['use_histograms'] = True
        self.tree_params_['hist_nbins'] = 256
        self.tree_params_['use_gpu'] = False
        self.tree_params_['gpu_id'] = 0
        self.tree_params_['parallel_by_example'] = False
        self.tree_params_['select_probability'] = 1.0
        self.params_['tree_params'] = self.tree_params_

        # define ridge regression model defaults
        self.ridge_params_['regularizer'] = 1.0
        self.ridge_params_['num_threads'] = 1
        self.ridge_params_['fit_intercept'] = False
        self.ridge_params_['select_probability'] = 1.0 - self.tree_params_['select_probability']
        self.params_['ridge_params'] = self.ridge_params_

        # define kernel approximator (rbf sampler) defaults
        self.kernel_params_['gamma'] = 1.0
        self.kernel_params_['n_components'] = 10
        self.kernel_params_['num_threads'] = 1
        self.params_['kernel_params'] = self.kernel_params_
        
        if params is not None:
        
            params_keys = params.keys()
            
            # Check if the user provided keys are supported (first level)
            library_first_level_keys = list(self.params_.keys())
            unsupported_keys = list(np.setdiff1d(list(params_keys), library_first_level_keys))
            if len(unsupported_keys) > 0:
                raise KeyError("Unsupported keys in the user-defined parameters dictionary: ", unsupported_keys)
            
            # Check if the user provided keys are supported (second level)
            for params_type in library_first_level_keys:
                if params_type in params_keys:
                    user_keys = list(params[params_type].keys())
                    library_keys = list(self.params_[params_type].keys())
                    unsupported_keys = list(np.setdiff1d(user_keys, library_keys))
                    if len(unsupported_keys) > 0:
                        raise KeyError('Unsupported keys in the user-defined {} parameters: {}'.format(params_type, unsupported_keys))
            
            '''
            Boosting-model-specific parameters
            '''
            if 'boosting_params' in params_keys:
                for var in params['boosting_params'].keys():
                    _param_check(BoostingMachine.PARAMS['boosting_params'], var, params['boosting_params'][var])
                    self.params_['boosting_params'][var] = params['boosting_params'][var]

            '''
            Tree-model-specific parameters
            '''
            if 'tree_params' in params_keys:
                for var in params['tree_params'].keys():
                    _param_check(BoostingMachine.PARAMS['tree_params'], var, params['tree_params'][var])
                    self.params_['tree_params'][var] = params['tree_params'][var]
            
            '''
            Ridge-regression-model-specific parameters
            '''
            if 'ridge_params' in params_keys:
                for var in params['ridge_params'].keys():
                    _param_check(BoostingMachine.PARAMS['ridge_params'], var, params['ridge_params'][var])
                    self.params_['ridge_params'][var] = params['ridge_params'][var]

            '''
            RBF-Sampler-model-specific parameters
            '''
            if 'kernel_params' in params_keys:
                for var in params['kernel_params'].keys():
                    _param_check(BoostingMachine.PARAMS['kernel_params'], var, params['kernel_params'][var])
                    self.params_['kernel_params'][var] = params['kernel_params'][var]

            # Check for dependencies
            if self.params_['tree_params']['max_max_depth'] < self.params_['tree_params']['min_max_depth']:
                raise ValueError("Parameter tree_params:max_max_depth should be >= tree_params_:min_max_depth.")

            if self.params_['tree_params']['use_gpu'] == True and self.params_['tree_params']['use_histograms'] == False:
                raise ValueError("GPU acceleration can only be enabled if tree_params:use_histograms parameter is True.")

            if (self.params_['ridge_params']['select_probability'] + self.params_['tree_params']['select_probability'] != 1.0):
                # print warning only if explicitely set by the user
                if 'select_probability' in params['ridge_params'].keys():
                    print("The sum of the tree and ridge selection probabilities should be 1.0. Updating probabilities proba(ridge) = 1 - proba(tree).")
                self.params_['ridge_params']['select_probability'] = 1.0 - self.params_['tree_params']['select_probability']

        self.model_ = np.array([], dtype=np.float32)
        self.model_size_ = 0

    def __getstate__(self):
        # reset ptr
        self.ptr = np.array([], dtype=np.uint64)
        return self.__dict__

    def get_params(self):

        """
        Get the values of the model parameters.

        Returns
        -------
        params : dict
        """

        return self.params_

    def import_model(self, input_file, type):

        """
        Import a pre-trained ensemble from the given input file of the given type.

        Supported import formats include PMML, ONNX, XGBoost json and lightGBM text. The
        corresponding input file types to be provided to the import_model function are
        'pmml', 'onnx', 'xgb_json', and 'lightgbm' respectively.

        If the input file contains features that are not supported by the import function
        then a runtime error is thrown indicating the feature and the line number within
        the input file containing the feature.

        Parameters
        ----------
        input_file : str
            Input filename

        type : {'pmml', 'onnx', 'xgb_json', 'lightgbm'}
            Input file type

        Returns
        -------
        self : object
        """

        if (not isinstance(input_file, (str))) or (input_file == ""):
                raise Exception("Input file name not provided.")

        if (not isinstance(type, (str))) or (type == ""):
                raise Exception("Input file type not provided.")

        out_ = libsnapml.booster_import(input_file, type)

        self.model_ = out_[0]
        self.model_size_ = out_[1]['model_size']
        self.ensemble_size_ = out_[1]['ensemble_size']
        self.params_['boosting_params']['base_score'] = out_[1]['base_score']
        self.params_['boosting_params']['num_round'] = out_[1]['ensemble_size']
        self.params_['boosting_params']['learning_rate'] = out_[1]['learning_rate']

        return self

    def fit(self, X_train, y_train, sample_weight=None, X_val=None, y_val=None, sample_weight_val=None):

        """
        Fit the model according to the given train data.

        Parameters
        ----------
        X_train : dense matrix (ndarray)
            Train dataset

        y_train : array-like, shape = (n_samples,)
            The target vector corresponding to X_train.

        sample_weight : array-like, shape = (n_samples,)
            Training sample weights

        X_val : dense matrix (ndarray)
            Validation dataset

        y_val : array-like, shape = (n_samples,)
            The target vector corresponding to X_val.

        sample_weight_val : array-like, shape = (n_samples,)
            Validation sample weights

        Returns
        -------
        self : object
        """

        # Boosting Machine model random state
        #if (self.params_['boosting_params']['random_state'] == None):
        #    # Not sure if this should be the random state
        #    random_state = np.random.get_state()[1][0]
        #else:
        #random_state = self.params_['boosting_params']['random_state']

        # the user has not set the base score, thus we will set it so that it speeds up the learning
        if self.params_['boosting_params']['base_score'] is None:
        
            # this is a regression problem        
            if self.params_['boosting_params']['objective'] == 'mse':
                if sample_weight is None:
                    self.params_['boosting_params']['base_score'] = np.average(y_train)
                else:
                    self.params_['boosting_params']['base_score'] = np.average(y_train, weights=sample_weight)
        
            elif self.params_['boosting_params']['objective'] == 'cross_entropy':
                p = np.average(y_train) if sample_weight is None else np.average(y_train, weights=sample_weight)
                self.params_['boosting_params']['base_score'] = -np.log(1.0/p-1.0)

            # this is a classification problem
            else:  
                if sample_weight is None:
                    sum_positives = np.sum(y_train > 0)
                    sum_negatives = y_train.shape[0] - sum_positives
                    self.params_['boosting_params']['base_score'] = np.log(sum_positives/sum_negatives) if sum_negatives > 0 and sum_positives > 0 else 0.0
                else:
                    sum_positives = np.sum(sample_weight[y_train > 0])
                    sum_negatives = np.sum(sample_weight) - sum_positives
                    self.params_['boosting_params']['base_score'] = np.log(sum_positives/sum_negatives) if sum_negatives > 0 and sum_positives > 0 else 0.0
                    
        if type(X_train).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        if X_val is not None and type(X_val).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        # helper function to prep data
        def prep_data(X, y, name):
            num_ft = 0
            num_nz = 0
            indptr = np.array([])
            indices = np.array([])
            data = np.array([])
            labs = np.array([])

            # get number of examples/features
            num_ex = X.shape[0]
            num_ft = X.shape[1]

            # in most cases, y_train should contain all examples
            if len(y) != num_ex:
                raise ValueError("Inconsistent dimensions: X.shape[0] must equal len(y)")

            num_nz    = num_ex * num_ft
            data      = np.ascontiguousarray(X, dtype=np.float32)
            indptr    = np.array([])
            indices   = np.array([])

            labs = y.astype(np.float32)

            return num_ex, num_ft, num_nz, indptr, indices, data, labs

        # prepare training data
        train_num_ex, train_num_ft, train_num_nz, train_indptr, train_indices, train_data, train_labs = prep_data(X_train, y_train, "train")

        # prepare validation data
        if X_val is not None and y_val is not None:
            val_num_ex, val_num_ft, val_num_nz, val_indptr, val_indices, val_data, val_labs = prep_data(X_val, y_val, "val")
        else:
            val_num_ex, val_num_ft, val_num_nz, val_indptr, val_indices, val_data, val_labs = 0, 0, 0, np.array([]), np.array([]), np.array([]), np.array([])

        if not sample_weight is None:
            if type(sample_weight).__name__ != "ndarray":
                raise TypeError("Parameter sample_weight: invalid type. Supported type: ndarray.")
            sample_weight = sample_weight.astype(np.float32)
        else:
            sample_weight = np.array([], dtype=np.float32)

        if not sample_weight_val is None:
            if type(sample_weight_val).__name__ != "ndarray":
                raise TypeError("Parameter sample_weight_val: invalid type. Supported type: ndarray.")
            if X_val is None:
                raise ValueError("Parameter sample_weight_val not supported when X_val and y_val are not defined.")
            sample_weight_val = sample_weight_val.astype(np.float32)
        else:
            sample_weight_val = np.array([], dtype=np.float32)


        '''
        if train_num_ft >= train_num_ex and self.params_['tree_params']['use_histograms']:
            print("Number of features is >= number of examples. Disabling histogram-based optimizations.")
            self.params_['tree_params']['use_histograms']=False
        '''

        out_ = libsnapml.booster_fit(self.params_['boosting_params'],
                                     self.params_['tree_params'],
                                     self.params_['ridge_params'],
                                     self.params_['kernel_params'],
                                     train_num_ex, train_num_ft, train_num_nz,
                                     train_indptr, train_indices, train_data, train_labs,
                                     val_num_ex, val_num_ft, val_num_nz,
                                     val_indptr, val_indices, val_data, val_labs,
                                     sample_weight, sample_weight_val)

        self.model_ = out_[0]
        self.model_size_ = out_[1]['model_size']
        self.ensemble_size_ = out_[1]['best_num_rounds']
        self.n_features_in_ = train_num_ft

        return None


    def _predict(self, X, get_proba, num_threads=1):

        """
        Raw predictions

        If the training objective is 'mse' then it returns the predicted estimates.
        If the training objective is 'logloss' or 'cross_entropy' then it returns the predicted estimates
        before the logistic transformation (raw logits).

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        get_proba : flag that indicates if output probabilities are to be computed
            0 : get raw predictions
            1 : get output probabilities (only for predict proba)

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimates.
        """

        if type(X).__name__ != "ndarray":
            raise TypeError("Tree-based models in Snap ML only support numpy.ndarray")

        if hasattr(self, "n_features_in_") and X.shape[1] != self.n_features_in_:
            raise ValueError("Predict was passed %d features, but model was trained with %d features"
                                        % (X.shape[1], self.n_features_in_))

        num_ex = 0
        num_ft = 0
        indptr = np.array([])
        indices =  np.array([])
        data = np.array([])

        num_ex = X.shape[0]
        num_ft = X.shape[1]

        # Keep the sparsity checks for future support for sparse datasets
        if (type(X).__name__ != "ndarray"):
            raise ValueError("X should be in ndarray format.")

        data      = X.astype(np.float32)
        data      = np.ascontiguousarray(data)    # enforce row-major format
        indptr    = np.array([])
        indices   = np.array([])

        pred = []

        # Generate predictions
        pred, ptr = libsnapml.booster_predict(num_ex,
                                         num_ft,
                                         indptr,
                                         indices,
                                         data,
                                         self.params_['boosting_params']['num_round'],
                                         self.params_['boosting_params']['learning_rate'],
                                         self.params_['boosting_params']['colsample_bytree'],
                                         self.params_['kernel_params']['n_components'],
                                         self.params_['boosting_params']['random_state'],
                                         self.params_['boosting_params']['base_score'],
                                         self.model_,
                                         self.model_size_,
                                         get_proba,
                                         self.params_['ridge_params']['fit_intercept'],
                                         self.params_['kernel_params']['gamma'],
                                         num_threads,
                                         self.ptr_)

        if ptr is not None:
            self.ptr_ = ptr

        pred = np.array(pred)

        if not np.all(np.isfinite(pred)):
            warnings.warn("Boosting diverged; Try using a smaller learning rate.")

        # handle case of divergence
        pred = np.nan_to_num(pred)

        return pred


    def predict(self, X, num_threads=1):

        """
        Raw predictions

        If the training objective is 'mse' then it returns the predicted estimates.
        If the training objective is 'logloss' or 'cross_entropy' then it returns the predicted estimates
        before the logistic transformation (raw logits).

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimates.
        """

        return self._predict(X, 0, num_threads)



    def predict_proba(self, X, num_threads=1):

        """
        Output probabilities

        Use only if the training objective is 'logloss' (i.e., for binary classification problems).
        It returns the probabilities of each sample belonging to each class. 
        The probabilities are calculated using the logistic transformation. 

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for predicting class estimates.

        num_threads : int
            Number of threads to use for prediction.

        Returns
        -------
        proba: array-like, shape = (n_samples, 2)
            Returns the predicted probabilities of each sample belonging to each class.
        """
        return self._predict(X, 1, num_threads)


    def compress_trees(self, X):

        """
        Compress decision trees for fast inference

        The binary decision tree ensemble created by training or by importing a pre-trained
        model is transformed into a more compact (compressed) format that enables higher inference
        performance and a smaller serialized model size.

        The transformation involves organizing the original binary decision trees into node clusters
        with specific interconnection structures based on expected node access characteristics. By
        exploiting the interconnection and node characteristics, the node clusters can be compressed
        within a minimum number of cache lines while also increasing spatial locality and, thus,
        cache performance.

        The input data set (currently mandatory, optional in next release) is used to predict node
        access characteristics for performing the node clustering.

        Parameters
        ----------
        X : dense matrix (ndarray)
            Dataset used for compressing trees

        """

        num_ex = X.shape[0]
        num_ft = X.shape[1]

        # Validate data type
        if (type(X).__name__ == "ndarray"):
            data = X.astype(np.float32)
            data = np.ascontiguousarray(data)    # enforce row-major format
        else:
            raise ValueError("X should be in ndarray format.")

        # Compress trees
        out = libsnapml.booster_compress(num_ex,
                                         num_ft,
                                         data,
                                         self.params_['boosting_params']['num_round'],
                                         self.model_,
                                         self.model_size_)

        self.model_ = out[0]
        self.model_size_ = out[1]['model_size']

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

if sys.version_info[0] < 3:
    import libsnapmllocal2 as libsnapml
else:
    import snapml.libsnapmllocal3 as libsnapml

from abc import ABC, abstractmethod

from snapml.CommonModel import CommonModel

class RandomForest(CommonModel):

    @abstractmethod
    def __init__(self):
        # just for reference
        self.n_estimators = None
        self.criterion = None
        self.max_depth = None
        self.min_samples_leaf = None
        self.max_features = None
        self.bootstrap = None
        self.n_jobs = None
        self.random_state = None
        self.verbose = None
        self.use_histograms = None
        self.hist_nbins = None
        self.use_gpu = None
        self.gpu_ids = None
        self.task_type_ = None
        self.params = None
        self.n_features_in_ = None

    def check_gpu(self):
        if (self.use_gpu == True) and (self.max_depth is None or self.max_depth > 16):
            print("GPU acceleration only supported for bounded max_depth <= 16; forest will be built with max_depth=16")
            self.max_depth = 16

        self.gpu_ids = np.array(self.gpu_ids).astype(np.uint32)
        if self.use_gpu and len(self.gpu_ids) == 0:
            raise ValueError("Please provide at least one gpu_id.")

        for gpu_id in self.gpu_ids:
            if gpu_id < 0:
                raise ValueError("Invalid gpu_id")

    def c_fit(self,
              max_depth,
              min_samples_leaf,
              max_features,
              random_state,
              num_ex,
              num_ft,
              num_nz,
              indptr,
              indices,
              data,
              labs,
              sample_weight):   
        return libsnapml.rfc_fit(self.task_type_,
                                self.n_estimators,
                                self.criterion,
                                max_depth,
                                min_samples_leaf,
                                max_features,
                                self.bootstrap,
                                self.n_jobs,
                                random_state,
                                self.verbose,
                                self.use_histograms,
                                self.hist_nbins,
                                self.use_gpu,
                                self.gpu_ids,
                                num_ex,
                                num_ft,
                                num_nz,
                                indptr,
                                indices,
                                data,
                                labs,
                                sample_weight)


    def c_predict(self,
                  num_ex,
                  num_ft,
                  indptr,
                  indices,
                  data,
                  n_jobs,
                  proba):

        # Generate predictions
        return libsnapml.rfc_predict(self.task_type_,
                                     self.n_estimators,
                                     num_ex,
                                     num_ft,
                                     n_jobs,
                                     indptr,
                                     indices,
                                     data,
                                     self.model_,
                                     self.model_size_,
                                     proba)


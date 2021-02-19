#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Thu 10 Jan 2019 07:38:10 PM CST

# File Name: utils.py
# Description:

"""

import numpy as np
import pandas as pd
import scipy
from sklearn.neighbors import NearestNeighbors, KNeighborsRegressor


def reassign_cluster_with_ref(Y_pred, Y):
    """
    Reassign cluster to reference labels
    Inputs:
        Y_pred: predict y classes
        Y: true y classes
    Return:
        f1_score: clustering f1 score
        y_pred: reassignment index predict y classes
        indices: classes assignment
    """
    def reassign_cluster(y_pred, index):
        y_ = np.zeros_like(y_pred)
        for i, j in index:
            y_[np.where(y_pred==i)] = j
        return y_
    from sklearn.utils.linear_assignment_ import linear_assignment
#     assert Y_pred.size == Y.size
    D = max(Y_pred.max(), Y.max())+1
    w = np.zeros((D,D), dtype=np.int64)
    for i in range(Y_pred.size):
        w[Y_pred[i], Y[i]] += 1
    ind = linear_assignment(w.max() - w)

    return reassign_cluster(Y_pred, ind)



def mixingMetric(data, batch_id, k = 5, k_max = 100, percent_cells = 0.2):
    """
    For each cell, we examine the (k.max =100) ranked nearest neighbors across all datasets. 
    We also compute the k=5 closest neighbors for each dataset individually. We then ask which rank in 
    the overall neighborhood list corresponds to the 5th neighbor in each dataset (with a max of 300), 
    and took a median over all these values. This corresponds to a mixing metric per cell, and we averaged 
    across all cells.
    """
#     print("Start calculating MixingMetric score")
    n_neighbors = min(k_max, len(data) - 1)
    nne = NearestNeighbors(n_neighbors=1 + n_neighbors, n_jobs=8)
    nne.fit(data)
    distances, indices = nne.kneighbors(data)
    indices = np.delete(indices,0,1) 
    
    batches_ = np.unique(batch_id)
    n_batches = len(batches_)
    if n_batches < 2:
        raise ValueError("Should be more than one cluster for batch mixing")
    near_batch = np.zeros(n_batches)
    score = 0
    
    indx = np.random.choice(np.arange(data.shape[0]), size=int(percent_cells*data.shape[0]), replace=False)
    indices = indices[indx]
    for i in range(len(indx)):
        for j in range(n_batches):
            if len(np.where(batch_id[indices[i]] == batches_[j]).__getitem__(0)) < k:
                near_batch[j] = n_neighbors;
            else:
                near_batch[j] = np.where(batch_id[indices[i]] == batches_[j]).__getitem__(0)[k-1]
        score += np.median(near_batch)  

    score = int(score // float(len(indx)))
    score = float('0.'+str(score))
    return score


def entropy_batch_mixing(data, batches, n_neighbors=100, n_pools=100, n_samples_per_pool=100):
    """
    First calculate the regional mixing entropies at the location of 100 randomly chosen cells from all batches
    Second define 100 nearest neighbors for each randomly chosen cell
    Third the mean mixing entropy was then calculated as the mean of the regional entropies
    Fourth repeat this procedure for 100 iterations with different randomly chosen cells.
    """
#     print("Start calculating Entropy mixing score")
    def entropy(batches):
        p = np.zeros(N_batches)
        adapt_p = np.zeros(N_batches)
        a = 0
        for i in range(N_batches):
            p[i] = np.mean(batches == batches_[i])
            a = a + p[i]/P[i]
        entropy = 0
        for i in range(N_batches):
            adapt_p[i] = (p[i]/P[i])/a
            entropy = entropy - adapt_p[i]*np.log(adapt_p[i]+10**-8)
        return entropy

    n_neighbors = min(n_neighbors, len(data) - 1)
    nne = NearestNeighbors(n_neighbors=1 + n_neighbors, n_jobs=8)
    nne.fit(data)
    kmatrix = nne.kneighbors_graph(data) - scipy.sparse.identity(data.shape[0])

    score = 0
    batches_ = np.unique(batches)
    N_batches = len(batches_)
    if N_batches < 2:
        raise ValueError("Should be more than one cluster for batch mixing")
    P = np.zeros(N_batches)
    for i in range(N_batches):
            P[i] = np.mean(batches == batches_[i])
    for t in range(n_pools):
        indices = np.random.choice(np.arange(data.shape[0]), size=n_samples_per_pool)
        score += np.mean([entropy(batches[kmatrix[indices].nonzero()[1]
                                                 [kmatrix[indices].nonzero()[0] == i]])
                          for i in range(n_samples_per_pool)])
    Score = score / float(n_pools)
    return Score / float(np.log2(N_batches))


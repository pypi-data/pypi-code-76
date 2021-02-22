import pandas as pd
import numpy as np
from feature_engine.selection import DropConstantFeatures
from feature_engine.selection import DropDuplicateFeatures
from feature_engine.selection import DropCorrelatedFeatures, SmartCorrelatedSelection
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

def dropconstant(df, tol=0.998, variables=[]):
    if(len(variables)==0):
        sel = DropConstantFeatures(tol=tol, variables=None, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp
    if(len(variables)!=0):
        sel = DropConstantFeatures(tol=tol, variables=variables, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp


def dropduplicated(df, variables=[]):
    if(len(variables)==0):
        sel = DropDuplicateFeatures(variables=None, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp
    if(len(variables)!=0):
        sel = DropDuplicateFeatures(variables=variables, missing_values='raise')
        sel.fit(df)
        tmp = sel.transform(df)
        return tmp


def dropcorrelated(df, threshold=0.8):
    sel = DropCorrelatedFeatures(threshold=threshold, method='pearson', missing_values='raise')
    sel.fit(df)
    tmp = sel.transform(df)
    return tmp


def smart_dropcorrelated(trainfeatures,target,testfeatures,model,threshold=0.8):
    sel = SmartCorrelatedSelection(variables=None, method="pearson", threshold=threshold, missing_values="raise",
            selection_method="model_performance", estimator=model, scoring="roc_auc", cv=3)
    sel.fit(trainfeatures,target)
    tmp = sel.transform(testfeatures)
    return tmp


def step_forward(features,target,model,kfeatures, info=False):
    sfs = SFS(model, k_features=kfeatures, forward=True, floating=False, verbose=2, scoring='roc_auc',cv=3)
    sfs = sfs.fit(np.array(features), target)
    if(info):
        selected_feat = features.columns[list(sfs.k_feature_idx_)]
        return selected_feat.to_list()



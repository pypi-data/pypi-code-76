from feature_engine.encoding import RareLabelEncoder
from feature_engine.imputation import MeanMedianImputer, ArbitraryNumberImputer, EndTailImputer, CategoricalImputer, RandomSampleImputer, AddMissingIndicator
from feature_engine.encoding import OneHotEncoder, OrdinalEncoder
from feature_engine import transformation as vt
from feature_engine.discretisation import EqualFrequencyDiscretiser, EqualWidthDiscretiser
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer

import pandas as pd

def all_functions():
    print("-imput_missing():\tfit, transform, method, arbitrary_number, distribution, tail")
    print("\t\t+Methods: median, mean, arbitrary, tail, mode, category, random, indicato\n")
    print("-group_rare_labels():\tfit, transform, tol, categories\n")
    print("-encoding():\tfit, transform, top_categories, drop_last, method, variables\n")
    print("-transform():\tdf, method, variables\n")
    print("-discretization():\tfit, transform, method, variables, return_object, return_boundaries, bins\n")
    print("-scale():\tdf, method\n")

def imput_missing(fit, transform, method='random', arbitrary_number=-999,distribution='iqr',tail='right',variables=[]):
    
    if(method=='median'):
        if(len(variables)==0):
            imputer = MeanMedianImputer(imputation_method='median')
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = MeanMedianImputer(imputation_method='median',variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        
    if(method=='mean'):
        if(len(variables)==0):
            imputer = MeanMedianImputer(imputation_method='mean')
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = MeanMedianImputer(imputation_method='mean',variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        
    if(method=='arbitrary'):
        if(len(variables)==0):
            imputer = ArbitraryNumberImputer(arbitrary_number=arbitrary_number)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = ArbitraryNumberImputer(arbitrary_number=arbitrary_number,variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
    
    if(method=='tail'):
        if(len(variables)==0):
            imputer = EndTailImputer(imputation_method=distribution,tail=tail)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = EndTailImputer(imputation_method=distribution,tail=tail,variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
    
    if(method=='mode'):   #CATEGORIC
        if(len(variables)==0):
            imputer = CategoricalImputer(imputation_method='frequent')
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = CategoricalImputer(imputation_method='frequent',variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
    
    if(method=='category'):   #CATEGORIC
        if(len(variables)==0):
            imputer = CategoricalImputer()
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = CategoricalImputer(variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
    
    if(method=='random'):
        if(len(variables)==0):
            imputer = RandomSampleImputer(random_state=0)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = RandomSampleImputer(random_state=0,variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
    
    if(method=='indicator'):   #CATEGORIC
        if(len(variables)==0):
            imputer = AddMissingIndicator()
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp
        if(len(variables)!=0):
            imputer = AddMissingIndicator(variables=variables)
            imputer.fit(fit)
            tmp = imputer.transform(transform)
            return tmp


def group_rare_labels(fit,transform,tol=0.05,categories=4):
    rare_encoder = RareLabelEncoder(tol=tol,n_categories=categories)
    rare_encoder.fit(fit.to_frame())
    tmp = rare_encoder.transform(transform.to_frame())
    return tmp


def encoding(fit,transform,method='onehot',top_categories=None,drop_last=True,variables=[]):
    
    if(method=='onehot'):
        if(len(variables)==0):
            ohe_enc = OneHotEncoder(top_categories=None,drop_last=drop_last)
            ohe_enc.fit(fit)
            tmp = ohe_enc.transform(transform)
            return tmp
        if(len(variables)!=0):
            ohe_enc = OneHotEncoder(top_categories=None,drop_last=drop_last,variables=variables)
            ohe_enc.fit(fit)
            tmp = ohe_enc.transform(transform)
            return tmp
    
    if(method=='order'):
        if(len(variables)==0):
            ordinal_enc = OrdinalEncoder(encoding_method='arbitrary')
            ordinal_enc.fit(fit)
            tmp = ordinal_enc.transform(transform)
            return tmp
        if(len(variables)!=0):
            ordinal_enc = OrdinalEncoder(encoding_method='arbitrary',variables=variables)
            ordinal_enc.fit(fit)
            tmp = ordinal_enc.transform(transform)
            return tmp


def transform(df,method,variables=[]):
    
    if(method=='log'):
        if(len(variables)==0):
            lt = vt.LogTransformer()
            lt.fit(df)
            tmp = lt.transform(df)
            return tmp
        if(len(variables)!=0):
            lt = vt.LogTransformer(variables=variables)
            lt.fit(df)
            tmp = lt.transform(df)
            return tmp
    
    if(method=='exp'):
        if(len(variables)==0):
            et = vt.PowerTransformer()
            et.fit(df)
            tmp = et.transform(df)
            return tmp
        if(len(variables)!=0):
            et = vt.PowerTransformer(variables=variables)
            et.fit(df)
            tmp = et.transform(df)
            return tmp
    
    if(method=='inv'):
        if(len(variables)==0):
            rt = vt.ReciprocalTransformer()
            rt.fit(df)
            tmp = rt.transform(df)
            return tmp
        if(len(variables)!=0):
            rt = vt.ReciprocalTransformer(variables=variables)
            rt.fit(df)
            tmp = rt.transform(df)
            return tmp
    
    if(method=='boxcox'):
        if(len(variables)==0):
            bct = vt.BoxCoxTransformer()
            bct.fit(df)
            tmp = bct.transform(df)
            return tmp
        if(len(variables)!=0):
            bct = vt.BoxCoxTransformer(variables=variables)
            bct.fit(df)
            tmp = bct.transform(df)
            return tmp
    
    if(method=='yeo'):
        if(len(variables)==0):
            yjt = vt.YeoJohnsonTransformer()
            yjt.fit(df)
            tmp = yjt.transform(df)
            return tmp
        if(len(variables)!=0):
            yjt = vt.YeoJohnsonTransformer(variables=variables)
            yjt.fit(df)
            tmp = yjt.transform(df)
            return tmp

def discretization(fit,transform,method='equalfreq',variables=[],return_object=False,return_boundaries=False):
    
    if(method=='equalrange'):
        if(len(variables)==0):
            disc = EqualWidthDiscretiser(return_object=return_object,return_boundaries=return_boundaries)
            disc.fit(fit)
            tmp = disc.transform(transform)
            return tmp
        if(len(variables)!=0):
            disc = EqualWidthDiscretiser(return_object=return_object,return_boundaries=return_boundaries,variables=variables)
            disc.fit(fit)
            tmp = disc.transform(transform)
            return tmp
    
    if(method=='equalfreq'):
        if(len(variables)==0):
            disc = EqualFrequencyDiscretiser(return_object=return_object,return_boundaries=return_boundaries)
            disc.fit(fit)
            tmp = disc.transform(transform)
            return tmp
        if(len(variables)!=0):
            disc = EqualFrequencyDiscretiser(return_object=return_object,return_boundaries=return_boundaries,variables=variables)
            disc.fit(fit)
            tmp = disc.transform(transform)
            return tmp


def scale(df,method='minmax'):
    if(method=='standar'):
        scaler = StandardScaler()
        scaler.fit(df)
        tmp = scaler.transform(df)
        tmp = pd.DataFrame(tmp, columns=df.columns)
        return tmp
    if(method=='minmax'):
        scaler = MinMaxScaler()
        scaler.fit(df)
        tmp = scaler.transform(df)
        tmp = pd.DataFrame(tmp, columns=df.columns)
        return tmp
    if(method=='normal'):
        scaler = Normalizer(norm='l1')
        scaler.fit(df)
        tmp = scaler.transform(df)
        tmp = pd.DataFrame(tmp, columns=df.columns)
        return tmp



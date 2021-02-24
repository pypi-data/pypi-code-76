
from functools import partial
import pickle
import string
import re

import numpy as np
import pandas as pd
from pyspace.pandas.pdfunctions import pddisplay, pdselect

import sklearn
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
# from cleanlab.classification import LearningWithNoisyLabels
from sklearn.metrics import classification_report

import pyspace
from pyspace.sklearn.data_structure.dataset_wrapper import DatasetContainer
from pyspace.sklearn.pipeline import pipeline_grid
# from pyspace.sklearn.pipeline.PIPE_MAPPINGS import PIPE_MAPPINGS
from pyspace.sklearn.model_selection.supervised_selection import SupervisedSelection

try:
    from pyspace.nlp.toolkit.zemberek import lemmatize as zflemmatizer
    from pyspace.nlp.toolkit.zemberek import tokenize as zftokenizer
    from pyspace.nlp.toolkit.zemberek import normalize as zfnormalizer
except:
    pass
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.metrics import score_functions 
from pyspace.metrics import confusion_functions 

import sklearn
from sklearn.svm import LinearSVC

import numpy as np
from tensorflow import keras

# %%
import copy

# %%
from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin

try:
    from sklearn_hierarchical_classification.classifier import HierarchicalClassifier
except:
    import_sklearn_hierarchical_classification = False

from sklearn.preprocessing import LabelEncoder

# from tqdm.notebook import tqdm as notebook_tqdm
try:
    from tqdm import tqdm_notebook as notebook_tqdm
except:
    import_tqdm = False


class LinearSVCExtended(LinearSVC):
    
    def predict_proba(self,X,y=None):
        
        pred = self.predict(X)
        
        pred = [ np.where(self.classes_ == val)[0][0] for val in pred ]
        proba = keras.utils.to_categorical(pred, num_classes=len(self.classes_))
        
        return proba


class HierarchicalClassifierExtended(BaseEstimator, ClassifierMixin):
    
    ## TODO : each classifier metrics, list of nodes as keys
    
    def __init__(self, base_estimator=[], hierarchy_params=[{},np.array([])], labelencoder_params=[np.array([]),np.array([])], enable_notebook_tqdm=False):
        if(enable_notebook_tqdm):
            progress_wrapper = notebook_tqdm
        else:
            progress_wrapper = None
            
        assert hierarchy_params[1].all() == labelencoder_params[0].all()
        
        self.hierarchy_params = hierarchy_params
        self.hierarchy = HierarchyManager(hierarchy_params[0], leaf_vocab=hierarchy_params[1])
        if(self.hierarchy == []):
            class_hierarchy = []
        else:
            class_hierarchy = self.hierarchy.adjacency_dict_of_lists
            
        self.clf = HierarchicalClassifier(base_estimator=base_estimator, class_hierarchy=class_hierarchy, progress_wrapper=progress_wrapper)
        
        self.labelencoder_params = labelencoder_params
        temp = LabelEncoder()
        temp.fit(labelencoder_params[0])
        assert labelencoder_params[0].all() == temp.classes_.all() 
        assert labelencoder_params[1].all() == temp.transform(labelencoder_params[0]).all()
        self.labelencoder = temp
        
        self.classes_ = self.labelencoder.transform(labelencoder_params[0])
        
        
    def fit(self, X, y=None):
        y = self.labelencoder.inverse_transform(y)
        self.clf.fit(X, y)
        return self
    
    def predict(self,X,y=None):
        y_pred = self.clf.predict(X)
        y_pred = self.labelencoder.transform(y_pred)
        
        return y_pred
    
    def predict_proba(self,X,y=None):
        
        # if(hasattr(self.clf, 'predict_proba')):
        #     proba = self.clf.predict_proba(X)
        # else:
        #     pred = self.predict(X)
        #     pred = [ np.where(self.labelencoder.transform(self.labelencoder.classes_) == val)[0][0] for val in pred ]
        #     proba = keras.utils.to_categorical(pred, num_classes=len(self.labelencoder.classes_))
            
        proba = self.clf.predict_proba(X)
        return proba

    def set_params(self, **params):
        self.__init__(**params)
            
    def predict_level_1(self, X, y):
        
        y = self.labelencoder.inverse_transform(y)
        
        intent_tree_dict = self.hierarchy.leaf_to_level1
        
        y_true = [intent_tree_dict[x] if x in intent_tree_dict else x for x in y]
        y_pred = clf.clf.graph_.nodes['<ROOT>']['classifier'].predict(X)

        labelencoder = LabelEncoder()
        
        target_names = list(set(y_pred).union(set(y_true)))
        labelencoder.fit(target_names)

        y_true = labelencoder.transform(y_true)
        y_pred = labelencoder.transform(y_pred)
        
        return y_true, y_pred, labelencoder
    
    
class HierarchyManager():
    def __init__(self, data, mode=0, leaf_vocab=None):
        if(mode == 0):
            if(str(type(leaf_vocab)) != str(type(None))):
                data = HierarchyManager.clear_intent_tree(data, leaf_vocab)
            
            self.nested_dicts = data
            self.adjacency_dict_of_lists = HierarchyManager.get_adjacency_dict_of_lists(self.nested_dicts)
            self.leaves = HierarchyManager.get_leaves(self.nested_dicts)
            self.leaf_to_level1 = HierarchyManager.get_leaf_to_level1(self.nested_dicts)
            
        pass
    
    @staticmethod
    def get_adjacency_dict_of_lists(dict1):

        def get_adjacency_recursion(dict1):
            result = {}

            for key in dict1:
                if(dict1[key] == {}):
                    pass
                else:
                    result[key] = list(dict1[key].keys())
                    result = {**result, **get_adjacency_recursion(dict1[key])}
                    pass

            return result
        class_hierarchy = {'<ROOT>': list(dict1.keys())}
        for level1 in dict1:
            class_hierarchy[level1] = list(dict1[level1].keys())
            class_hierarchy = {**class_hierarchy, **get_adjacency_recursion(dict1[level1])}

        return class_hierarchy

    @staticmethod
    def get_leaves(dict1):
        result = []

        for key in dict1:
            if(dict1[key] == {}):
                result.append(key)
            else:
                result.extend(HierarchyManager.get_leaves(dict1[key]))
        return result
    
    @staticmethod
    def get_leaf_to_level1(intent_tree):
        intent_tree_dict = {}
        for level1 in intent_tree:
            l1_intents = HierarchyManager.get_leaves(intent_tree[level1])

            for l1_intent in l1_intents:

                intent_tree_dict[l1_intent] = level1
        return intent_tree_dict
    
    @staticmethod
    def test_data():
        temp_dict = {
            "A": {
                "1":{}, 
                "7":{}
            },
            "B": {
                "C":{
                    "3":{
                        "10":{
                            "11":{}
                        }
                    }, 
                    "8":{}
                }, 
                "9":{}
            },
        }
        
        return temp_dict

    @staticmethod
    def clear_intent_tree(bilmis_intent_tree, y_classes):
        bilmis_intent_tree = copy.deepcopy(bilmis_intent_tree)
        while True:
            # nonlocal _del_count
            _del_count = 0

            def f1(tree):
                nonlocal _del_count
                keys = list(tree.keys())

                for key in keys:

                    if tree[key] == {}:

                        if key not in y_classes:
                            del tree[key]
                            _del_count += 1
                            # print(_del_count)
                    else:
                        f1(tree[key])



            f1(bilmis_intent_tree)

            if _del_count == 0:
                break
        return bilmis_intent_tree


class BoWCalibratedSVC(BaseEstimator, ClassifierMixin):

    def __init__(self, ):
        
        pass
        
        
    def fit(self, X, y=None, n_jobs=8, verbose=1):
        
        from pyspace.sklearn.pipeline.PIPE_MAPPINGS import PIPE_MAPPINGS
        df = X.copy()[['Text', 'Intent']]

        dataset = DatasetContainer([[df, df['Intent'].values], 0, 0, 0])
        dataset.encode_labels()

        vocab = None

        #############################################################################

        preprocessconfig = [
            {'pdseries':{}},
            {'pdvalues':{}},
            {'onsent':{"func":[xNormalizer.clean_text], "multi":[True]}},
            {'onsent':{"func":[zfnormalizer]}},
            {'tokenize':{"tokenize_func":[partial(zftokenizer,mode=1)]}},
            {'ontoken':{"func":[zflemmatizer]}},
        ]

        default_parameters = {'tfidf': {'tokenizer':[lambda x: x], 'preprocessor':[lambda x: x], 'vocabulary':[vocab]},}
        config = [
                {'pandas': [
                    (['Text'], [ 
                        *preprocessconfig,
                        {'tfidf': {'ngram_range':[(1,1)], 'min_df':[1], **default_parameters['tfidf'] }},
                    ]),
                    (['Text'], [
                        *preprocessconfig[:-1],
                        {'tfidf': {'ngram_range':[(1,1)], 'min_df':[1], **default_parameters['tfidf'] }},
                    ]),
                ]},
            ]
        
        #############################################################################

        key_exclude_grid={'models': ['pdvalues', 'pdseries', 'npfloat64', 'toarray'], 'modelparams': {'tfidf': ['tokenizer', 'preprocessor', 'vocabulary'], 'tf': ['tokenizer', 'preprocessor'], 'labelfittedtfidf': ['tfidf'], 'fasttextwordvector': ['ft'] }}

        pipelines = pipeline_grid.generate_pipegrid(PIPE_MAPPINGS, config, key_exclude_grid=key_exclude_grid)
        pkeys = list(pipelines.keys())

        #############################################################################

        dataset.train.dataspace = pipeline_grid.fit_transform_pipegrid(pipelines, dataset)
        dkeys = list(dataset.train.dataspace.keys())
        
        #############################################################################
        models = {
            'clsvm': CalibratedClassifierCV,
        }
        params = {
            'clsvm': {'base_estimator':[LinearSVC(random_state=0)],
                    'cv':[StratifiedKFold(n_splits=5, shuffle=True, random_state=0)], },
        }

        #############################################################################

        sup = SupervisedSelection([dataset.train.dataspace, dataset.train.dataspace], models, params)
        sup.fit(cv=1, repeat=1, n_jobs=n_jobs, verbose=verbose,   ) 

        self.dataset = dataset
        self.pipeline = pipelines[pkeys[0]]
        self.pipeline_grid = pipeline_grid
        self.clf = sup.results_raw.iloc[0]['clf']

        return self
    
    def predict(self,X,y=None):

        return self.dataset.labelencoder.inverse_transform(
            self.clf.predict( 
                self.pipeline.transform( 
                    pd.DataFrame(X, 
                                columns=['Text'])) ))
    
    def predict_proba(self,X,y=None):
        
        return self.clf.predict_proba( 
                self.pipeline.transform( 
                    pd.DataFrame(X, 
                                columns=['Text'])) )
            

    def set_params(self, **params):
        self.__init__(**params)
    
class FasttextClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, ):
        import fasttext
        self.fasttext = fasttext
        
    def generate_fasttext_data(self, X, y, fasttext_datapath='./fasttext_dataset.txt'):
        def write_fastext_dataset(X, y, path):
            # Create dataset
            with open(path, "w+", encoding='utf-8') as file:
                for text, label in zip(X, y):
                    file.write(f'__label__{label} {text}\n')

        # self.le = LabelEncoder()
        # y = self.le.fit_transform(y)

        write_fastext_dataset(X, y, fasttext_datapath)
        
        return fasttext_datapath


    def fit(self, X, y=None, epoch=60, dim=80, minn=4, maxn=6, wordNgrams=2):
        
        fasttext_dataset = self.generate_fasttext_data(X, y)
        fasttextparameters = {
            'epoch' : epoch,
            'dim' : dim,
            'minn' : minn,
            'maxn' : maxn,
            'wordNgrams' : wordNgrams,
        }
        self.clf = self.fasttext.train_supervised(input=fasttext_dataset, **fasttextparameters)
   
        return self
    
    def predict(self,X,y=None):

        y_pred = self.clf.predict(X, k=1)[0]
        y_pred = [p[0] for p in y_pred]
        return y_pred
        
    def predict_proba(self,X,y=None):
        
        y_pred_proba = np.array(ft.predict([tt,tt], k=-1)[1]) 
        return y_pred_proba
    


class CalibratedFasttext(BaseEstimator, ClassifierMixin):

    def __init__(self, ):
        import fasttext
        # self.clf = CalibratedClassifierCV( , cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0))
        
        
    def fit(self, X, y=None, n_jobs=8, verbose=1):

        
        return self
    
    def predict(self,X,y=None):

        return self.dataset.labelencoder.inverse_transform(
            self.clf.predict( 
                self.pipeline.transform( 
                    pd.DataFrame(X, 
                                columns=['Text'])) ))
    
    def predict_proba(self,X,y=None):
        
        return self.clf.predict_proba( 
                self.pipeline.transform( 
                    pd.DataFrame(X, 
                                columns=['Text'])) )
            

    def set_params(self, **params):
        self.__init__(**params)
    


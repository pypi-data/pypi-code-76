# %%
import pandas as pd
import numpy as np
try:
    import seaborn as sns
except:
    pass

from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

from collections import Counter
import time
import copy

# %%
from pyspace.sklearn.pipeline import pipeline_grid


# %%
class ClusterSelection:
    
    def __init__(self, dataspace, modelspace):
        self.dataspace = dataspace
        self.modelspace = modelspace
        
    def fit(self, targetlabelid=0, verbose=1):
        
        self.results = []
        
        for dkey in self.dataspace.keys():
            
            if(verbose):
                print(time.strftime("%H:%M - %Ss") + ' ### ' + dkey + ' '*(40 - len(dkey)) + ' ###')
                
            for mkey in self.modelspace.keys():
                
                if(verbose):
                    print(time.strftime("%H:%M - %Ss") + ' ### ' + '#'*7 + ' ' + mkey + ' '*(32 - len(mkey)) + ' ###')
                    
                paramgrid = list(ParameterGrid(self.modelspace[mkey]['paramgrid']))
                
                for params in paramgrid:
                    
                    model = self.modelspace[mkey]['model'](**params)
                    preds = model.fit_predict(self.dataspace[dkey]['X'])
                    scores = ClusterSelection.get_cluster_metrics(self.dataspace[dkey]['y'], preds, targetlabelid)
                    
                    self.results.append({**{'data':dkey, 'model':mkey, 'params':str(params), 'modelobject':model,
                                            'preds': preds, 
                                            'labels': self.dataspace[dkey]['y']
                                                      if type(self.dataspace[dkey]['y']) != type(None) else [-1]*len(preds)
                                           },
                                         **scores})
                    

        self.results = pd.DataFrame(self.results)
        self.results = self.results.sort_values(['fmi_precision'], ascending=False)
        
        self.summary = self.results.copy()
        self.summary = self.summary[['f1_macro', 'f1_weighted', 'accuracy',
                                     'fmi_precision',
                                     'data', 'model', 'params', 
                                    ]].copy()
        
    @staticmethod
    def get_cluster_metrics(true, pred, labelid):
        def fmi_precision(true, pred):
            n_samples = len(true)
            c = metrics.cluster.contingency_matrix(true, pred, sparse=True)
            tk = np.dot(c.data, c.data) - n_samples
            pk = np.sum(np.asarray(c.sum(axis=0)).ravel() ** 2) - n_samples
            qk = np.sum(np.asarray(c.sum(axis=1)).ravel() ** 2) - n_samples
            
            precision = tk / pk
            recall = tk / qk
            
            # precision * recall harmonic mean
            fmi = np.sqrt(precision) * np.sqrt(recall) if tk != 0. else 0.

            return precision
        def fmi_precision_by_label(true, pred, labelid):
            c = metrics.cluster.contingency_matrix(true, pred)
            c = c[:,c[labelid,:] / np.asarray(c.sum(axis=0)).ravel() > 0.3]
            n_samples = np.sum(c.ravel())
            tk = np.dot(c.ravel(), c.ravel()) - n_samples
            pk = np.sum(np.asarray(c.sum(axis=0)).ravel() ** 2) - n_samples
            qk = np.sum(np.asarray(c.sum(axis=1)).ravel() ** 2) - n_samples
            
            precision = tk / pk
            recall = tk / qk
            
            # precision * recall harmonic mean
            fmi = np.sqrt(precision) * np.sqrt(recall) if tk != 0. else 0.

            return precision
        def fmi_precision_by_label_v2(true, pred, labelid):
            c = metrics.cluster.contingency_matrix(true, pred)
            c = c[:,c[labelid,:] / np.asarray(c.sum(axis=0)).ravel() > 0.9]
            
            precision_v2 = np.sum(c[labelid,:])
            return precision_v2
        def fmi_precision_by_label_v3(true, pred, labelid):
            c = metrics.cluster.contingency_matrix(true, pred)
            c = c[:,c[labelid,:] / np.asarray(c.sum(axis=0)).ravel() == 1]
            
            precision_v2 = np.sum(c[labelid,:])
            return precision_v2
        def fmi_precision_by_label_v4(true, pred, labelid):
            c = metrics.cluster.contingency_matrix(true, pred)
            c = c[:,c[labelid,:] / np.asarray(c.sum(axis=0)).ravel() == 1]
            
            if(c.shape[1] == 0):
                precision_v2 = 0
            else:
                precision_v2 = np.max(c[labelid,:])
            return precision_v2
        
        def sklearn_classification_report(true, pred):
            default_label = Counter(true).most_common()[0][0]
            
            le2 = LabelEncoder()
            pred_enc = le2.fit_transform(pred)
            
            coo = metrics.cluster.contingency_matrix(true, pred_enc)
            
            cluster_to_label = dict(zip(le2.classes_, coo.argmax(axis=0) ))
            
            pred_label = [cluster_to_label[p] if p in cluster_to_label else default_label for p in pred]
            
            f1_macro = metrics.f1_score(true, pred_label, average='macro')
            f1_weighted = metrics.f1_score(true, pred_label, average='weighted')
            acc = metrics.accuracy_score(true, pred_label)
            
            return (f1_macro, f1_weighted, acc)
        
        clustermetrics = {
            "homogeneity" : metrics.homogeneity_completeness_v_measure(true, pred)[0] if type(true) != type(None) else -1,
            "completeness" : metrics.homogeneity_completeness_v_measure(true, pred)[1] if type(true) != type(None) else -1,
            "v_measure" : metrics.homogeneity_completeness_v_measure(true, pred)[2] if type(true) != type(None) else -1,
            "fmi" : metrics.fowlkes_mallows_score(true,pred) if type(true) != type(None) else -1,
            "ami" : metrics.adjusted_mutual_info_score(true, pred, average_method='arithmetic') if type(true) != type(None) else -1,
            "fmi_precision" : fmi_precision(true,pred) if type(true) != type(None) else -1,
            "fmi_precision_by_label" : fmi_precision_by_label(true, pred, labelid) if type(true) != type(None) else -1,
            "fmi_precision_by_label_v2" : fmi_precision_by_label_v2(true, pred, labelid) if type(true) != type(None) else -1,
            "fmi_precision_by_label_v3" : fmi_precision_by_label_v3(true, pred, labelid) if type(true) != type(None) else -1,
            "fmi_precision_by_label_v4" : fmi_precision_by_label_v4(true, pred, labelid) if type(true) != type(None) else -1,
            "f1_macro" : sklearn_classification_report(true, pred)[0] if type(true) != type(None) else -1,
            "f1_weighted" : sklearn_classification_report(true, pred)[1] if type(true) != type(None) else -1,
            "accuracy" : sklearn_classification_report(true, pred)[2] if type(true) != type(None) else -1,
        }

        return clustermetrics
    
    @staticmethod
    def get_contingency_matrix(true, pred, le1=None, le2=None):
        coo = metrics.cluster.contingency_matrix(true, pred)
        coo_df = pd.DataFrame(coo)
        # coo_df = coo_df.append(dict(zip(coo_df.columns,np.asarray(coo.sum(axis=0)).ravel())), ignore_index=True)
        
        if(le1):
            idx_df = pd.DataFrame(data=list(le1.classes_), index=list(le1.transfrom(le1.classes_)), columns=['   '],)
            coo_df = pd.merge(coo_df, idx_df, left_index=True, right_index=True)
            coo_df.set_index('   ', inplace=True)
            
        if(le2):
            coo_df.rename(columns=dict(zip(list(le2.transform(le2.classes_)), list(le2.classes_))), inplace=True)
        
        cm = sns.light_palette("green", as_cmap=True)
        coo_df_view = coo_df.style.background_gradient(cmap=cm)
        return coo_df_view, coo_df



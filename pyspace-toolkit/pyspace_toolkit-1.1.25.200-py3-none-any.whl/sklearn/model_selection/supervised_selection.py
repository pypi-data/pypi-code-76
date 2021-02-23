# %%
import pandas as pd
import numpy as np
try:
    import seaborn as sns
except:
    pass

from sklearn.model_selection import GridSearchCV, ParameterGrid
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

import gc
from collections import Counter
import time
import copy
from functools import partial
from joblib import Parallel, delayed

# TODO
# https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html

# %%
from pyspace.sklearn.pipeline import pipeline_grid


# %%
class SupervisedSelectionDeprecated:
    
    def __init__(self, dataspace, models, params):
        
        self.dataspace = dataspace
        self.models = models
        self.params = params
        self.grid_searches = {}
        
    def fit(self, cv=3, n_jobs=48, verbose=1, refit=False):
        
        if(cv == 1):
            cv = [(slice(None), slice(None))]
        else:
            cv = StratifiedKFold(n_splits=cv)
        
        scoring = {'f1': metrics.make_scorer(metrics.f1_score, average='weighted'),
                   'acc': metrics.make_scorer(metrics.accuracy_score)}
        # sklearn.metrics.precision_score
        # sklearn.metrics.roc_auc_score
        
        for datakey in self.dataspace:
            if(verbose):
                print(time.strftime("%H:%M - %Ss") + ' ### ' + datakey + ' '*(40 - len(datakey)) + ' ###')
            
            for modelkey in self.models.keys():
                
                if(verbose):
                    print(time.strftime("%H:%M - %Ss") + ' ### ' + '#'*7 + ' ' + modelkey + ' '*(32 - len(modelkey)) + ' ###')

                model = self.models[modelkey]()
                params = self.params[modelkey]
                gs = GridSearchCV(model, params, cv=cv, n_jobs=n_jobs, verbose=0, scoring=scoring, refit=refit, return_train_score=True)
                gs.fit(self.dataspace[datakey]['X'],self.dataspace[datakey]['y'])
                self.grid_searches[(datakey,modelkey)] = gs
        
        self.summary = self.score_summary()
        
    def score_summary(self):
        
        def get_grid_search_scores(grid_search, metric):
            scores = []
            
            cv = grid_search.cv
            if(cv == [(slice(None, None, None), slice(None, None, None))] ):
                cv = 1
            elif(str(type(cv)) != str(type(1))):
                cv = cv.get_n_splits()
            
            for i in range(cv):
                resultkey = "split{}_test_".format(i) + metric
                scores.append(grid_search.cv_results_[resultkey])
            
            scores = np.array(scores).T
            return scores
        
        summary_df = pd.DataFrame()
        
        for k in self.grid_searches:
            
            rowsummary = {}
            rowsummary['data'] = k[0]
            rowsummary['estimator'] = k[1]
            params = self.grid_searches[k].cv_results_['params']
            f1scores = get_grid_search_scores(self.grid_searches[k], 'f1')
            accscores = get_grid_search_scores(self.grid_searches[k], 'acc')
            
            for params_i, f1scores_i, accscores_i in zip(params, f1scores, accscores):
                rowsummary_i = copy.deepcopy(rowsummary)
                rowsummary_i['params'] = params_i
                
                rowsummary_i['f1_mean_score'] = np.mean(f1scores_i)
                rowsummary_i['f1_max_score'] = np.max(f1scores_i)
                rowsummary_i['acc_mean_score'] = np.mean(accscores_i)
                rowsummary_i['acc_max_score'] = np.max(accscores_i)
            
                summary_df = summary_df.append(rowsummary_i, ignore_index=True)
                
        summary_df = summary_df.sort_values(['f1_mean_score'], ascending=False)
        summary_df = summary_df[['data','estimator','params','acc_max_score','f1_max_score','acc_mean_score','f1_mean_score']]
        return summary_df


# %%

class SupervisedSelectionNoParallel:

    # from joblib import Parallel, delayed
    
    # parallel = Parallel(n_jobs=self.n_jobs, verbose=self.verbose,pre_dispatch=self.pre_dispatch)
    # out = parallel(
    #     delayed(_fit_and_score)(clone(base_estimator),X, y,train=train, test=test,parameters=parameters,**fit_and_score_kwargs)
    #     for parameters, (train, test) in product(candidate_params,cv.split(X, y, groups)) 
    # )
 
    def __init__(self, dataspace, models, params):
        
        self.dataspace = dataspace
        self.models = models
        self.params = params
        
    def fit(self, cv=5, repeat=1, verbose=1,):
        
        results = []
        
        scoring = {'f1': partial(metrics.f1_score, average='weighted'),
                   'acc': metrics.accuracy_score}
        
        # sklearn.metrics.precision_score
        # sklearn.metrics.roc_auc_score
        
        datakeys = self.dataspace[0].keys()
        
        for datakey in datakeys:
            if(verbose):
                print(time.strftime("%H:%M - %Ss") + ' ### ' + datakey + ' '*(40 - len(datakey)) + ' ###')
        
            modelkeys = self.models.keys()
            for modelkey in modelkeys:
        
                if(verbose):
                    print(time.strftime("%H:%M - %Ss") + ' ### ' + '#'*7 + ' ' + modelkey + ' '*(32 - len(modelkey)) + ' ###')

                paramgrid = list(ParameterGrid(self.params[modelkey]))
                    
                for params in paramgrid:
                    
                    if(verbose):
                        print(time.strftime("%H:%M - %Ss") + ' ### ' + '#'*7 + ' ' + '#'*7 + ' ' + str(params) + ' '*(24 - len(str(params))) + ' ###')

                    if cv == 1 or cv == None:
                        
                        X = self.dataspace[0][datakey]['X']
                        y = self.dataspace[0][datakey]['y']
                        X_test = self.dataspace[1][datakey]['X']
                        y_test = self.dataspace[1][datakey]['y']
                        
                        model = self.models[modelkey](**params)
    
                        model.fit(X, y)
                        y_pred = model.predict(X_test)
                        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else [1] * len(y_pred)

                        y_true = y_test
                        
                        scores = {k:scoring[k](y_true, y_pred) for k in scoring}
                        
                        
                        results.append({**{'data':datakey, 
                                           'model':modelkey, 
                                           'params':str(params),
                                           'y_pred': y_pred, 
                                           'y_pred_proba': y_pred_proba,
                                           'y_true': y_true,
                                           'clf':model,
                                       },
                                     **scores})
                
                    else:
                        seed = 0
                        random_state = np.random.RandomState(seed)
                        
                        for repeat_index in range(repeat):
                        
                            skf = StratifiedKFold(n_splits=cv, random_state=random_state, shuffle=True)

                            X = self.dataspace[0][datakey]['X']
                            y = self.dataspace[0][datakey]['y']

                            for cv_index, (train_index, test_index) in enumerate(skf.split(y,y)):                    
                                model = self.models[modelkey](**params)

                                model.fit(X[train_index], y[train_index])
                                y_pred = model.predict(X[test_index])
                                y_pred_proba = model.predict_proba(X[test_index]) if hasattr(model, 'predict_proba') else [1] * len(y_pred)

                                y_true = y[test_index]

                                scores = {k:scoring[k](y_true, y_pred) for k in scoring}

                                results.append({**{'data':datakey, 
                                                   'model':modelkey, 
                                                   'params':str(params),
                                                   'repeat': repeat_index,
                                                   'cv': cv_index,
                                                   'train_index': train_index,
                                                   'test_index': test_index,
                                                   'y_pred': y_pred,
                                                   'y_pred_proba': y_pred_proba,
                                                   'y_true': y_true,
                                                   'clf':model,
                                               },
                                             **scores})
                
        results_raw = results
        self.results_raw = pd.DataFrame(results_raw)
        
        self.results = self.get_results(results_raw)
        self.summary = self.get_summary(results_raw)
        
    def get_summary(self, results_raw):
        
        df = pd.DataFrame(results_raw)
        
        group_cols = ['data', 'model', 'params',]
        metric_cols = list(set(list(df.columns)).difference({'data', 'model', 'params', 'repeat', 'cv', 'train_index', 'test_index' 'y_pred', 'y_pred_proba', 'y_true', 'clf'}))
        aggs = df.groupby(group_cols)[metric_cols].mean().reset_index()
        
        return aggs
        
    def get_results(self, results_raw):
        
        if 'cv' not in results_raw[0]:
            return pd.DataFrame(results_raw)
        
        df = pd.DataFrame(results_raw)
        
        group_cols = ['data', 'model', 'params',]
        metric_cols = list(set(list(df.columns)).difference({'data', 'model', 'params', 'repeat', 'cv', 'train_index', 'test_index' 'y_pred', 'y_pred_proba', 'y_true', 'clf'}))

        aggs = df.groupby(group_cols)[metric_cols].mean() #.reset_index()
        aggs['y_true'] = None
        
        for repeat_index in list(set(df['repeat'].values)):
            aggs['y_pred'+'_'+str(repeat_index)] = None
            aggs['y_pred_proba'+'_'+str(repeat_index)] = None

        for entry, group in df.groupby(group_cols):
            
            for repeat_index in list(set(df['repeat'].values)):
                
                temp = []
                for idx, row in group[group['repeat']==repeat_index].iterrows():
                    # temp.append((row['test_index'], row['y_true'], row['y_pred']))
                    tempdf = pd.DataFrame()
                    tempdf['test_index'] = row['test_index']
                    tempdf['y_true'] = row['y_true']
                    tempdf['y_pred'] = row['y_pred']
                    tempdf['y_pred_proba'] = list(row['y_pred_proba'])
                    temp.append(tempdf)

                tempdf = pd.concat(temp, ignore_index=True)
                tempdf = tempdf.sort_values(by=['test_index'], ascending=True)

                y_true = tempdf['y_true'].values
                y_pred = tempdf['y_pred'].values
                y_pred_proba = tempdf['y_pred_proba'].values # TODO np.vstack()

                # assert np.all(y_true == dataset.labelencoder.transform(dataset.train.y))
                # assert np.all(y_true == dataset.train.dataspace[dkeys[0]]['y'])
                datakeys = list(self.dataspace[0].keys())
                assert np.all(y_true == self.dataspace[0][datakeys[0]]['y'])

                ######################################################################################
                ######################################################################################

                aggs.at[entry, "y_true"] = y_true
                aggs.at[entry, "y_pred"+"_"+str(repeat_index)] = y_pred
                aggs.at[entry, "y_pred_proba"+"_"+str(repeat_index)] = y_pred_proba

        aggs = aggs.reset_index()
        
        ######################################################################################
        ######################################################################################
        
        aggs['y_pred_all'] = None
        aggs['y_true_all'] = None
        
        for result_index in list(aggs.index):
            
            y_pred_all = []
            y_true_all = []
            
            for col in list(aggs.columns):
                if col.startswith('y_pred') and not col.startswith('y_pred_proba') and not col.startswith('y_pred_all'):
                    y_pred_all += list(aggs.loc[result_index][col])
                    y_true_all += list(aggs.loc[result_index]['y_true'])
            aggs.at[result_index, 'y_pred_all'] = y_pred_all
            aggs.at[result_index, 'y_true_all'] = y_true_all

        ######################################################################################
        ######################################################################################
        
        return aggs


# %%

class SupervisedSelection:

    # TODO # wrappers in model creation; CalibratedClassifierCV, RFE, RFECV
    """
        models = {
            # 'svm': SVC, # 0.9152
            # 'lsvm': PIPE_MAPPINGS['lsvm'], # PIPE_MAPPINGS['lsvm+'] # 0.923643
            # 'hc': PIPE_MAPPINGS['hierarchic'], # 0.923985 # 0.925355
            # 'hc_1': PIPE_MAPPINGS['hierarchic'], # 0.917708
            # 'mlp': MLPClassifier
            'clsvm': CalibratedClassifierCV,# 0.917195
            # # #'clsvm_1': CalibratedClassifierCV, # 0.801633
        }
        params = {
            'svm': {'kernel':['linear']},
            'lsvm': {},
            'hc':{'base_estimator':[PIPE_MAPPINGS['lsvm+'](random_state=0)], 
                'hierarchy_params':[[data_hierarchy_temp, dataset.labelencoder.classes_]],  'labelencoder_params':[[dataset.labelencoder.classes_, dataset.labelencoder.transform(dataset.labelencoder.classes_)]], 'enable_notebook_tqdm':[True]},
            'hc_1':{'base_estimator':[CalibratedClassifierCV(PIPE_MAPPINGS['lsvm+'](random_state=0), cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0))], 
                'hierarchy_params':[[temp, dataset.labelencoder.classes_]],  'labelencoder_params':[[dataset.labelencoder.classes_, dataset.labelencoder.transform(dataset.labelencoder.classes_)]], 'enable_notebook_tqdm':[True]},
            'mlp': {'random_state':[0], 'hidden_layer_sizes':[(140),], 'batch_size':[16],  'max_iter':[20,]},
            'clsvm': {'base_estimator':[LinearSVC(random_state=0)],
                    'cv':[StratifiedKFold(n_splits=5, shuffle=True, random_state=0)], },
            'clsvm_1': {'base_estimator':[ PIPE_MAPPINGS['hierarchic'](base_estimator=PIPE_MAPPINGS['lsvm+'](random_state=0),
                                                                    hierarchy_params=[data_hierarchy_temp, dataset.labelencoder.classes_], 
                                                                    labelencoder_params=[dataset.labelencoder.classes_, dataset.labelencoder.transform(dataset.labelencoder.classes_)], 
                                                                    ),
                                    ],
                    'cv':[StratifiedKFold(n_splits=5, shuffle=True, random_state=0)], },
        }

        modelspace = {
            # 'cv':[2, StratifiedKFold(n_splits=2, shuffle=False, random_state=None)]
            'lsvm' : {
                'model': LinearSVC,
                'params': {},
                'wrappers' : [
                    ['rfecv', 'estimator', {'step':[40], 'min_features_to_select':[2000], 'cv':[StratifiedKFold(n_splits=5, shuffle=True, random_state=0)]}],
                    ['calibratedcv', 'base_estimator', {'cv':[StratifiedKFold(n_splits=5, shuffle=True, random_state=0)]}], 
                ],
            }
        }
    """
    def __init__(self, dataspace, models, params):
        
        self.dataspace = dataspace
        self.models = models
        self.params = params
        
    def fit(self, cv=5, repeat=1, keep_model=False, verbose=1, n_jobs=1, pre_dispatch='n_jobs', batch_size='auto', backend=None, prefer=None, require=None):
        
        results = []
        
        scoring = {'f1': partial(metrics.f1_score, average='weighted'),
                   'acc': metrics.accuracy_score}
        
        # sklearn.metrics.precision_score
        # sklearn.metrics.roc_auc_score
        
        def f_no_cv(datakey, modelkey, params):
            
            X = self.dataspace[0][datakey]['X']
            y = self.dataspace[0][datakey]['y']
            X_test = self.dataspace[1][datakey]['X']
            y_test = self.dataspace[1][datakey]['y']

            model = self.models[modelkey](**params)

            model.fit(X, y)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else [1] * len(y_pred)

            y_true = y_test

            scores = {k:scoring[k](y_true, y_pred) for k in scoring}


            return {**{'data':datakey, 
                               'model':modelkey, 
                               'params':str(params),
                               'y_pred': y_pred, 
                               'y_pred_proba': y_pred_proba,
                               'y_true': y_true,
                               'clf':model,
                           },
                         **scores}
        
        def f_cv(datakey, modelkey, params, repeat_index, cv_index, train_index, test_index):
            gc.collect(); gc.collect(); gc.collect();
            
            X = self.dataspace[0][datakey]['X']
            y = self.dataspace[0][datakey]['y']
            
            # params = {c:copy.deepcopy(v) for c,v in params.items()}
            model = self.models[modelkey](**params)

            model.fit(X[train_index], y[train_index])
            y_pred = model.predict(X[test_index])
            y_pred_proba = model.predict_proba(X[test_index]) if hasattr(model, 'predict_proba') else [1] * len(y_pred)

            y_true = y[test_index]

            scores = {k:scoring[k](y_true, y_pred) for k in scoring}

            if(not keep_model):
                del model
                model = None
                
                
            return {**{'data':datakey, 
                               'model':modelkey, 
                               'params':str(params),
                               'repeat': repeat_index,
                               'cv': cv_index,
                               'train_index': train_index,
                               'test_index': test_index,
                               'y_pred': y_pred,
                               'y_pred_proba': y_pred_proba,
                               'y_true': y_true,
                               'clf':model,
                           },
                         **scores}

        _fit = None
        config = []
        
        #########################################################
        #########################################################
        for datakey in self.dataspace[0].keys():
            for modelkey in self.models.keys():
                for params in list(ParameterGrid(self.params[modelkey])):
                    
                    
                    if cv == 1 or cv == None:
                        _fit = f_no_cv
                        
                        ############################################
                        ############################################
                        ############################################
                        
                        config.append((datakey, modelkey, params))
                
                    else:
                        _fit = f_cv

                        ############################################
                        ############################################
                        ############################################
                        
                        y = self.dataspace[0][datakey]['y']
                        
                        seed = 0
                        random_state = np.random.RandomState(seed)
                        for repeat_index in range(repeat):
            
                            skf = StratifiedKFold(n_splits=cv, random_state=random_state, shuffle=True)
                            for cv_index, (train_index, test_index) in enumerate(skf.split(y,y)):   
                                
                                config.append((datakey, modelkey, params, repeat_index, cv_index, train_index, test_index))
        #########################################################
        #########################################################
        
        # parallel = Parallel(verbose=verbose, n_jobs=n_jobs, pre_dispatch=pre_dispatch, batch_size=batch_size, backend=backend, prefer=prefer, require=require )        
        with Parallel(verbose=verbose, n_jobs=n_jobs, pre_dispatch=pre_dispatch, batch_size=batch_size, backend=backend, prefer=prefer, require=require ) as parallel:
            results = parallel(delayed(_fit)(*c_i) for c_i in config)                                
        
        gc.collect(); gc.collect(); gc.collect();
        
        results_raw = results
        self.results_raw = pd.DataFrame(results_raw)
        
        self.results = self.get_results(results_raw)
        self.summary = self.get_summary(results_raw)
        
    def get_summary(self, results_raw):
        
        df = pd.DataFrame(results_raw)
        
        group_cols = ['data', 'model', 'params',]
        metric_cols = list(set(list(df.columns)).difference({'data', 'model', 'params', 'repeat', 'cv', 'train_index', 'test_index' 'y_pred', 'y_pred_proba', 'y_true', 'clf'}))
        aggs = df.groupby(group_cols)[metric_cols].mean().reset_index()
        
        return aggs
        
    def get_results(self, results_raw):
        
        if 'cv' not in results_raw[0]:
            return pd.DataFrame(results_raw)
        
        df = pd.DataFrame(results_raw)
        
        group_cols = ['data', 'model', 'params',]
        metric_cols = list(set(list(df.columns)).difference({'data', 'model', 'params', 'repeat', 'cv', 'train_index', 'test_index' 'y_pred', 'y_pred_proba', 'y_true', 'clf'}))

        aggs = df.groupby(group_cols)[metric_cols].mean() #.reset_index()
        aggs['y_true'] = None
        
        for repeat_index in list(set(df['repeat'].values)):
            aggs['y_pred'+'_'+str(repeat_index)] = None
            aggs['y_pred_proba'+'_'+str(repeat_index)] = None

        for entry, group in df.groupby(group_cols):
            
            for repeat_index in list(set(df['repeat'].values)):
                
                temp = []
                for idx, row in group[group['repeat']==repeat_index].iterrows():
                    # temp.append((row['test_index'], row['y_true'], row['y_pred']))
                    tempdf = pd.DataFrame()
                    tempdf['test_index'] = row['test_index']
                    tempdf['y_true'] = row['y_true']
                    tempdf['y_pred'] = row['y_pred']
                    tempdf['y_pred_proba'] = list(row['y_pred_proba'])
                    temp.append(tempdf)

                tempdf = pd.concat(temp, ignore_index=True)
                tempdf = tempdf.sort_values(by=['test_index'], ascending=True)

                y_true = tempdf['y_true'].values
                y_pred = tempdf['y_pred'].values
                y_pred_proba = tempdf['y_pred_proba'].values # TODO np.vstack()

                # assert np.all(y_true == dataset.labelencoder.transform(dataset.train.y))
                # assert np.all(y_true == dataset.train.dataspace[dkeys[0]]['y'])
                datakeys = list(self.dataspace[0].keys())
                assert np.all(y_true == self.dataspace[0][datakeys[0]]['y'])

                ######################################################################################
                ######################################################################################

                aggs.at[entry, "y_true"] = y_true
                aggs.at[entry, "y_pred"+"_"+str(repeat_index)] = y_pred
                aggs.at[entry, "y_pred_proba"+"_"+str(repeat_index)] = y_pred_proba

        aggs = aggs.reset_index()
        
        ######################################################################################
        ######################################################################################
        
        aggs['y_pred_all'] = None
        aggs['y_true_all'] = None
        
        for result_index in list(aggs.index):
            
            y_pred_all = []
            y_true_all = []
            
            for col in list(aggs.columns):
                if col.startswith('y_pred') and not col.startswith('y_pred_proba') and not col.startswith('y_pred_all'):
                    y_pred_all += list(aggs.loc[result_index][col])
                    y_true_all += list(aggs.loc[result_index]['y_true'])
            aggs.at[result_index, 'y_pred_all'] = y_pred_all
            aggs.at[result_index, 'y_true_all'] = y_true_all

        ######################################################################################
        ######################################################################################
        
        return aggs



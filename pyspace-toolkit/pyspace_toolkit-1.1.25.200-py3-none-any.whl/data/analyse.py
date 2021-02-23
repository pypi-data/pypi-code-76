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
from pyspace.sklearn.pipeline.PIPE_MAPPINGS import PIPE_MAPPINGS
from pyspace.sklearn.model_selection.supervised_selection import SupervisedSelection

from pyspace.nlp.toolkit.zemberek import lemmatize as zflemmatizer
from pyspace.nlp.toolkit.zemberek import tokenize as zftokenizer
from pyspace.nlp.toolkit.zemberek import normalize as zfnormalizer
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.metrics import score_functions 
from pyspace.metrics import confusion_functions 


def get_cv_predictions(df, mode='text', cv=5, model_repeat_count=3, n_jobs=3, verbose=11,):

    df = df.copy()[['Text', 'Intent']]

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

    sup = SupervisedSelection([dataset.train.dataspace,], models, params)
    sup.fit(cv=cv, repeat=model_repeat_count, n_jobs=n_jobs, verbose=verbose,   ) 

    #############################################################################

    result_index = 0
    
    assert np.all(list(sup.results.iloc[result_index]['y_true']) == dataset.labelencoder.transform(dataset.train.y)) or np.all(list(sup.results.iloc[result_index]['y_true']) == dataset.labelencoder.transform(dataset.valid.y))
    assert np.all(list(sup.results.iloc[result_index]['y_true']) == dataset.train.dataspace[dkeys[0]]['y'])          or np.all(list(sup.results.iloc[result_index]['y_true']) == dataset.valid.dataspace[dkeys[0]]['y'])
    
    #############################################################################
    
    y_pred_repeated = sup.results.iloc[result_index]['y_pred_all']
    y_true_repeated = sup.results.iloc[result_index]['y_true_all']
    
    #############################################################################

    y_true =  sup.results.iloc[result_index]['y_true']

    #############################################################################
    
    y_prob_list = []
    for col in list(sup.results.columns):
        if col.startswith('y_pred_proba'):
            y_prob_list.append(np.vstack(sup.results.iloc[result_index][col]))
            
    y_prob_matrix_repeated = np.vstack(y_prob_list)
    y_prob_matrix_avg = sum(y_prob_list) / len(y_prob_list)

    #############################################################################

    # y_pred_repeated # comes from model
    y_pred_repeated_prob = [np.sort(row,)[::-1][0] for row in y_prob_matrix_repeated]

    y_2nd_pred_repeated = [np.argsort(row,)[::-1][1] for row in y_prob_matrix_repeated]
    y_2nd_pred_repeated_prob = [np.sort(row,)[::-1][1] for row in y_prob_matrix_repeated]
    
    y_3rd_pred_repeated = [np.argsort(row,)[::-1][2] for row in y_prob_matrix_repeated]
    y_3rd_pred_repeated_prob = [np.sort(row,)[::-1][2] for row in y_prob_matrix_repeated]

    #############################################################################

    y_pred_avg = [np.argsort(row,)[::-1][0] for row in y_prob_matrix_avg]
    y_pred_avg_prob = [np.sort(row,)[::-1][0] for row in y_prob_matrix_avg]

    y_2nd_pred_avg = [np.argsort(row,)[::-1][1] for row in y_prob_matrix_avg]
    y_2nd_pred_avg_prob = [np.sort(row,)[::-1][1] for row in y_prob_matrix_avg]
    
    y_3rd_pred_avg = [np.argsort(row,)[::-1][2] for row in y_prob_matrix_avg]
    y_3rd_pred_avg_prob = [np.sort(row,)[::-1][2] for row in y_prob_matrix_avg]

    #############################################################################
    y_true_repeated = dataset.labelencoder.inverse_transform(y_true_repeated)
    y_pred_repeated = dataset.labelencoder.inverse_transform(y_pred_repeated)
    y_2nd_pred_repeated = dataset.labelencoder.inverse_transform(y_2nd_pred_repeated)
    y_3rd_pred_repeated = dataset.labelencoder.inverse_transform(y_3rd_pred_repeated)

    y_true = dataset.labelencoder.inverse_transform(y_true)
    y_pred_avg = dataset.labelencoder.inverse_transform(y_pred_avg)
    y_2nd_pred_avg = dataset.labelencoder.inverse_transform(y_2nd_pred_avg)
    y_3rd_pred_avg = dataset.labelencoder.inverse_transform(y_3rd_pred_avg)
    #############################################################################

    y_prob_matrix_repeated_df = pd.DataFrame(y_prob_matrix_repeated, 
        columns=dataset.labelencoder.inverse_transform(list(range(y_prob_matrix_repeated.shape[1]))))
    y_prob_matrix_avg_df = pd.DataFrame(y_prob_matrix_avg, 
        columns=dataset.labelencoder.inverse_transform(list(range(y_prob_matrix_avg.shape[1]))))

    outdf_avg = df.copy()
    assert list(outdf_avg['Intent'].values) == list(y_true)
    # outdf_avg['y_true'] = y_true
    outdf_avg['y_pred'] = y_pred_avg
    outdf_avg['y_pred_prob'] = y_pred_avg_prob
    outdf_avg['y_2nd_pred_avg'] = y_2nd_pred_avg
    outdf_avg['y_2nd_pred_avg_prob'] = y_2nd_pred_avg_prob
    outdf_avg['y_3rd_pred_avg'] = y_3rd_pred_avg
    outdf_avg['y_3rd_pred_avg_prob'] = y_3rd_pred_avg_prob
    

    outdf_repeated = pd.concat([df.copy()]*model_repeat_count).reset_index(drop=True)
    assert list(outdf_repeated['Intent'].values) == list(y_true_repeated)
    # outdf_repeated['y_true'] = y_true_repeated
    outdf_repeated['y_pred'] = y_pred_repeated
    outdf_repeated['y_pred_prob'] = y_pred_repeated_prob
    outdf_repeated['y_2nd_pred_avg'] = y_2nd_pred_repeated
    outdf_repeated['y_2nd_pred_avg_prob'] = y_2nd_pred_repeated_prob
    outdf_repeated['y_3rd_pred_avg'] = y_3rd_pred_repeated
    outdf_repeated['y_3rd_pred_avg_prob'] = y_3rd_pred_repeated_prob

    # return ( outdf_avg, outdf_repeated, y_prob_matrix_avg_df, y_prob_matrix_repeated_df, dataset.labelencoder )
    return ( outdf_avg, y_prob_matrix_avg_df, )
    
def duplicate_analysis(tempdf, x_col, y_col):
    
    tempdf['__x_uncased'] = tempdf[x_col].apply(lambda x: xNormalizer.clean_text(x.lower().strip()))
    tempdf['__x_cased'] = tempdf[x_col].apply(lambda x: xNormalizer.clean_text(x.strip()))
    tempdf['__y'] = tempdf[y_col]
    
    text_duplication_uncased = tempdf.duplicated(['__x_uncased'], keep=False)
    text_duplication_cased = tempdf.duplicated(['__x_cased'], keep=False)
    text_intent_duplication = tempdf.duplicated(['__x_uncased', '__y'], keep=False)
    
    wrong_duplication = text_duplication_uncased & ~text_intent_duplication
    same_duplication_uncased = text_duplication_uncased & ~wrong_duplication & ~text_duplication_cased
    same_duplication_cased = text_duplication_cased & ~wrong_duplication & ~same_duplication_uncased
    
    
    duplicate_wrong_label_df = tempdf[wrong_duplication].sort_values('__x_uncased')
    duplicate_same_label_uncased_df = tempdf[same_duplication_uncased].sort_values('__x_uncased')
    duplicate_same_label_cased_df = tempdf[same_duplication_cased].sort_values('__x_uncased')
    
    tempdf.drop(columns=['__x_uncased','__x_cased','__y'], inplace=True)
    duplicate_wrong_label_df = duplicate_wrong_label_df.drop(columns=['__x_uncased','__x_cased','__y'])
    duplicate_same_label_uncased_df = duplicate_same_label_uncased_df.drop(columns=['__x_uncased','__x_cased','__y'])
    duplicate_same_label_cased_df = duplicate_same_label_cased_df.drop(columns=['__x_uncased','__x_cased','__y'])

    return duplicate_wrong_label_df, duplicate_same_label_uncased_df, duplicate_same_label_cased_df

def count_analysis(df, col):
    
    tvc = df[col].value_counts()
    tvcdf = pd.DataFrame(tvc)
    tvcdf = tvcdf.reset_index()
    tvcdf.columns = ['Intent', 'Sentence Count']
    
    tvcdfvc = tvcdf['Sentence Count'].value_counts()
    tvcdfvcdf = pd.DataFrame(tvcdfvc)
    tvcdfvcdf = tvcdfvcdf.reset_index()
    tvcdfvcdf.columns = ['Sentence Count*', 'Intent Count with Sentence Count*']
    tvcdfvcdf = tvcdfvcdf.sort_values('Sentence Count*')
    tvcdfvcdf = tvcdfvcdf.reset_index(drop=True)
    
    tfrqs = pd.concat([tvcdf, pd.DataFrame(columns=['',]), tvcdfvcdf, ], axis=1 )
    tfrqs = tfrqs.fillna("")
    return tfrqs
from functools import partial
import pickle
import string
import re

import numpy as np
import pandas as pd
from pyspace.pandas.pdfunctions import pddisplay, pdselect

from sklearn.preprocessing import LabelEncoder

import pyspace
from pyspace.metrics import score_functions 
from pyspace.metrics import confusion_functions 
from pyspace.data.analyse import duplicate_analysis, count_analysis
from pyspace.pandas.excel import pd_get_excel_formats, get_pair_confusion_document, pd_pair_confusion_set_border, pd_pair_confusion_to_excel, pd_excel_sheet_set_column_width, pd_to_excel

from cleanlab.classification import LearningWithNoisyLabels
from cleanlab.pruning import get_noise_indices



# def get_confusion_report(outdf_repeated, outdf, excel_file_path='./dataset_analysis.xlsx', y_prob_matrix=None, labelencoder=None):
def get_confusion_report(outdf, excel_file_path='./dataset_analysis.xlsx', y_prob_matrix_df=None,):
    assert ['Text','Intent','y_pred'] == list(outdf.columns)[:3]
    outdf_repeated = outdf.copy()

    model_repeat_count = outdf_repeated.shape[0] / outdf.shape[0]

    ###############################################################
    ## CLEANLAB
    ###############################################################
    # if str(type(y_prob_matrix)) != str(type(None)) and str(type(labelencoder)) != str(type(None)):
    #     numpy_array_of_noisy_labels = labelencoder.transform(outdf['Intent'])
    #     numpy_array_of_predicted_probabilities = y_prob_matrix
    if str(type(y_prob_matrix_df)) != str(type(None)):
        _classes = list(y_prob_matrix_df.columns)
        _class_map = dict(zip(_classes, list(range(len(_classes)))))
        numpy_array_of_noisy_labels = outdf['Intent'].replace(_class_map).values
        numpy_array_of_predicted_probabilities = y_prob_matrix_df.values

        ordered_label_errors = get_noise_indices(
            s=numpy_array_of_noisy_labels,
            psx=numpy_array_of_predicted_probabilities,
            frac_noise=1.0,
            sorted_index_method='normalized_margin', # Orders label errors
        )

        confident_labels = [l for l in list(range(numpy_array_of_predicted_probabilities.shape[0])) if l not in ordered_label_errors]
    else:
        ordered_label_errors= []
    cleanlab = outdf.iloc[ordered_label_errors]
    
    ###############################################################
    ## SCORES
    ###############################################################
    scores = score_functions.get_scores(outdf_repeated['Intent'], outdf_repeated['y_pred'])
    vc = dict(outdf['Intent'].value_counts())
    for i in outdf_repeated['y_pred'].unique():
        if i not in vc:
            vc[i] = 0
    score_report = score_functions.get_report(outdf_repeated['Intent'], outdf_repeated['y_pred'], vc= vc,  mode=0) 
    score_report = score_report[~( 
        (score_report['precision'] == 0) &
        (score_report['recall'] == 0) &
        (score_report['f1'] == 0) &
        (score_report['test count'] == 0) 
    )]
    
    
    ###############################################################
    ## CONFUSION
    ###############################################################
    temp = LabelEncoder().fit( list(outdf_repeated['Intent'])+list(outdf_repeated['y_pred']) )
    confusion = confusion_functions.get_confusion_analysis(temp.transform(outdf_repeated['Intent']), temp.transform(outdf_repeated['y_pred']), temp)

    ###############################################################
    ## DUPLICATE ANALYSIS
    ###############################################################
    dup_analysis = duplicate_analysis(outdf, 'Text', 'Intent')
    duplicate_wrong_label_df = dup_analysis[0] 
    duplicate_same_label_uncased_df = dup_analysis[1]
    duplicate_same_label_cased_df = dup_analysis[2]

    ###############################################################
    ## CONFUSED PAIRS
    ###############################################################
    pairs = []
    confusion_itp_head_count_v1 = 6
    confusion_i_threshold_v1 = 12
    
    confusion_head_count = 60
    
    confusion_itp_head_count_v2 = 20
    confusion_i_threshold_v2 = 4
    
    score_tail_count = 20
    score_tail_confusion_head_count = 6
    confusion_i_threshold_v3 = 1

    pairs.extend(confusion[confusion['<i>']>confusion_i_threshold_v1].sort_values('<i/t>', ascending=False).head(confusion_itp_head_count_v1)[['true','pred']].values)
    pairs.extend(confusion[confusion['<i>']>confusion_i_threshold_v1].sort_values('<i/p>', ascending=False).head(confusion_itp_head_count_v1)[['true','pred']].values)
    pairs.extend(confusion[['true','pred']].head(confusion_head_count).values)
    pairs.extend(confusion[confusion['<i>']>confusion_i_threshold_v2].sort_values('<i/t>', ascending=False).head(confusion_itp_head_count_v2)[['true','pred']].values)
    pairs.extend(confusion[confusion['<i>']>confusion_i_threshold_v2].sort_values('<i/p>', ascending=False).head(confusion_itp_head_count_v2)[['true','pred']].values)

    for p in score_report.iloc[-score_tail_count:]['i'].values:
        pairs.extend(pdselect(confusion,[['true', '==', p],['<i>','>',confusion_i_threshold_v3]]).head(score_tail_confusion_head_count)[['true','pred']].values)
        pairs.extend(pdselect(confusion,[['pred', '==', p],['<i>','>',confusion_i_threshold_v3]]).head(score_tail_confusion_head_count)[['true','pred']].values)

    pairs = [tuple(sorted(p)) for p in pairs]
    pairs = [ v for (i,v) in enumerate(pairs) if v not in pairs[0:i] ]

    confused_pairs = pairs

    ###############################################################
    ###############################################################

    with pd.ExcelWriter(excel_file_path) as writer:
        
        # temp_scores = pd.DataFrame(scores.values(), index=scores.keys(), columns=['scores'])
        temp_scores = pd.DataFrame(scores['accuracy    '], index=['accuracy    '], columns=['scores'])
        temp_intent_counts = count_analysis(outdf, 'Intent')
        temp_score_report = (score_report[['i', 'f1', 'test count']] if score_report.iloc[0]['test count'] < score_report.iloc[0]['train count'] else score_report[['i', 'f1', 'train count']] ).rename(columns={'i':'intent', 'f1':'f1 score'})
        temp_confusion = pdselect(confusion, [['<i/u>', '>', 0.01],['<i>', '>', 0],]).rename(columns={'true': 'doğru', 'pred': 'tahmin', 'count': 'kapılan', 'r. count': 'kaptırılan', '<i>': 'kapma', '<i/t>': 'kapma yüzdesi',})[['doğru', 'tahmin', 'kapma', 'kapma yüzdesi']] # ['<i/u>', '>', 0.05],['<i>', '>', 5]
        temp_confusion['kapma'] = temp_confusion['kapma'].apply(lambda x: round(x / model_repeat_count))
        # temp_pair_rename_config = {'Intent':'doğru','y_pred_0':'tahmin','_y_pred_proba_0':'tahmin*'}
        temp_pair_rename_config = {}
        
        
        workbook  = writer.book
        f1 = workbook.add_format({'bg_color':   '#fff5cc',}) # yellow
        f2 = workbook.add_format({'bg_color':   '#FFC7CE',}) # pink # '#ffebed'
        f3 = workbook.add_format({'bg_color':   '#f5f5f5',}) # gray # #f2f2f2 #E8E8E8
        f4 = workbook.add_format({'bg_color':   '#cff0fa',}) # blue # #cce2e8 #d4f6ff #cff0fa
        
        f5 = workbook.add_format({'bg_color':   '#C6EFCE',}) # green
        f6 = workbook.add_format({'bg_color':   '#e6f0e8',}) # green
        
        fpair = [f3, f6]
        
        
        # pd_to_excel(outdf[prob0].sort_values('Intent').rename(columns=temp_pair_rename_config), writer, 'results', index_bool=False)
        pd_to_excel(outdf.sort_values('Intent').rename(columns=temp_pair_rename_config), writer, 'results', index_bool=False)
        results_worksheet = writer.sheets['results']
        results_worksheet.conditional_format(1, 2, outdf.shape[0], 2 , {'type': 'cell', 'criteria':'==', 'value':'B2', 'format':f1})
        results_worksheet.conditional_format(1, 2, outdf.shape[0], 2 , {'type': 'cell', 'criteria':'!=', 'value':'B2', 'format':f2})
        
        current_row_idx = 1
        color_idx = 0
        for entry, group in outdf.groupby('Intent'):
            group_len = len(group)
            results_worksheet.conditional_format(current_row_idx, 1, current_row_idx + group_len -1, 1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':fpair[color_idx]})
            
            # color_idx = 1 - color_idx
            color_idx = (color_idx+1) % 2
            current_row_idx = current_row_idx + group_len
            
        results_worksheet.conditional_format(1, 3, outdf.shape[0], 3 , {'type': 'cell', 'criteria':'>=', 'value':'0.4', 'format':f5})
        results_worksheet.conditional_format(1, 3, outdf.shape[0], 3 , {'type': 'cell', 'criteria':'>=', 'value':'0.2', 'format':f3})
        results_worksheet.conditional_format(1, 3, outdf.shape[0], 3 , {'type': 'cell', 'criteria':'<=', 'value':'0.2', 'format':f2})
            
            
            
        pd_to_excel(temp_scores, writer, 'scores', _round=4)
        
        pd_to_excel(temp_score_report, writer, 'scores_per_intent')
        pd_to_excel(temp_confusion, writer, 'confusion', _round=2, index_bool=False) 
        
        # pd_to_excel(duplicate_wrong_label_df[base0].rename(columns=temp_pair_rename_config), writer, 'duplicate_wrong', index_bool=False) if len(duplicate_wrong_label_df) != 0 else None
        pd_to_excel(duplicate_wrong_label_df.rename(columns=temp_pair_rename_config), writer, 'duplicate_wrong', index_bool=False) if len(duplicate_wrong_label_df) != 0 else None
        
        
        for idx, p in enumerate(confused_pairs):
            # pd_pair_confusion_to_excel(outdf, p, writer, str(idx)+'_' + p[0][:12] + '__' + p[1][:12], wrong_n=100, same_n=100, other_n=30, rename_config = temp_pair_rename_config, base0=prob0, index_bool=False) # prob0
            pd_pair_confusion_to_excel(outdf, p, writer, str(idx)+'_' + p[0][:12] + '__' + p[1][:12], wrong_n=100, same_n=100, other_n=30, rename_config = temp_pair_rename_config, base0=list(outdf.columns), index_bool=False) # prob0
            
        
        # pd_to_excel(duplicate_same_label_cased_df[base0].rename(columns=temp_pair_rename_config), writer, 'duplicate_same_cased', index_bool=False) if len(duplicate_same_label_cased_df) != 0 else None
        pd_to_excel(duplicate_same_label_cased_df.rename(columns=temp_pair_rename_config), writer, 'duplicate_same_cased', index_bool=False) if len(duplicate_same_label_cased_df) != 0 else None
        # pd_to_excel(duplicate_same_label_uncased_df[base0].rename(columns=temp_pair_rename_config), writer, 'duplicate_same_uncased', index_bool=False) if len(duplicate_same_label_uncased_df) != 0 else None
        pd_to_excel(duplicate_same_label_uncased_df.rename(columns=temp_pair_rename_config), writer, 'duplicate_same_uncased', index_bool=False) if len(duplicate_same_label_uncased_df) != 0 else None
        
        # pd_to_excel(mistaken_sentences.rename(columns=temp_pair_rename_config), writer, 'mistaken_sentences', index_bool=False) if len(mistaken_sentences) != 0 else None
        pd_to_excel(cleanlab, writer, 'cleanlab_mistaken_sentences', index_bool=False) if len(cleanlab) != 0 else None
        
        pd_to_excel(temp_intent_counts, writer, 'intent_counts', _round=4, index_bool=False)
    
    ###############################################################


    pass
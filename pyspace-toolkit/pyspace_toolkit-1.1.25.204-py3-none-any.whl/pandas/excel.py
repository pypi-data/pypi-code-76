from functools import partial
import pickle
import string
import re

import numpy as np
import pandas as pd
from pyspace.pandas.pdfunctions import pddisplay, pdselect

def pd_get_excel_formats(writer, ):
    
    workbook  = writer.book
    # border_args = {'bottom':5, 'top':5, 'left':5, 'right':5}
    format0 = workbook.add_format({'top':1,})
    format0_2 = workbook.add_format({'top':5,})
    # Light red fill with dark red text.
    format1 = workbook.add_format({'bg_color':   '#FFC7CE',}) # pink
    format1_2 = workbook.add_format({'bg_color':   '#ffebed',})
    # Light yellow fill with dark yellow text.
    format2 = workbook.add_format({'bg_color':   '#FFEB9C',})
    format2_2 = workbook.add_format({'bg_color':   '#fff5cc',})
    # Green fill with dark green text.
    format3 = workbook.add_format({'bg_color':   '#C6EFCE', })
    format3_2 = workbook.add_format({'bg_color':   '#e6f0e8',})
    
    formats = [format0, format0_2, format1, format1_2, format2, format2_2, format3, format3_2]
    outf = [format1, format1_2, format3, format3_2, format2, format2, format2_2, format2_2, ]
    
    return formats, outf

def get_pair_confusion_document(df, pair, selected_cols, wrong_n=-1, same_n=10, other_n=3):

    pred_column = '' 
    if 'y_pred' in list(df.columns):
        pred_column = 'y_pred'
    elif 'y_pred_0' in list(df.columns):
        pred_column = 'y_pred_0'
    else:
        assert 1==0

    t0 = pdselect(df, [
        ['Intent', '==', pair[0] ],
        [pred_column, '==', pair[1] ],
    ])
    
    t1 = pdselect(df, [
        ['Intent', '==', pair[1] ],
        [pred_column, '==', pair[0] ],
    ])
    
    t2 = pdselect(df, [
        ['Intent', '==', pair[0] ],
        [pred_column, '==', pair[0] ],
    ])
    
    t3 = pdselect(df, [
        ['Intent', '==', pair[1] ],
        [pred_column, '==', pair[1] ],
    ])
    
    t4 = pdselect(df, [
        ['Intent', '==', pair[0] ],
        [pred_column, '!=', pair[0] ],
        [pred_column, '!=', pair[1] ],
    ])
    
    t5 = pdselect(df, [
        ['Intent', '==', pair[1] ],
        [pred_column, '!=', pair[0] ],
        [pred_column, '!=', pair[1] ],
    ])
    
    t6 = pdselect(df, [
        [pred_column, '==', pair[0] ],
        ['Intent', '!=', pair[0] ],
        ['Intent', '!=', pair[1] ],
    ])
    
    t7 = pdselect(df, [
        [pred_column, '==', pair[1] ],
        ['Intent', '!=', pair[0] ],
        ['Intent', '!=', pair[1] ],
    ])
    
    
    t0 = t0.sample(n=wrong_n, random_state=1)  if len(t0) > wrong_n and wrong_n != -1 else t0
    t1 = t1.sample(n=wrong_n, random_state=1)  if len(t1) > wrong_n and wrong_n != -1  else t1
    t2 = t2.sample(n=same_n, random_state=1)  if len(t2) > same_n else t2
    t3 = t3.sample(n=same_n, random_state=1)  if len(t3) > same_n else t3
    t4 = t4.sample(n=other_n, random_state=1)  if len(t4) > other_n else t4
    t5 = t5.sample(n=other_n, random_state=1)  if len(t5) > other_n else t5
    t6 = t6.sample(n=other_n, random_state=1)  if len(t6) > other_n else t6
    t7 = t7.sample(n=other_n, random_state=1)  if len(t7) > other_n else t7
    
    out = [t0,t1,t2,t3,t4,t6,t5,t7]
    
    outl = [0]
    for tt in out:
        outl.append(outl[-1] + len(tt))
    
    outdf = pd.concat(out)[selected_cols]
    
    return outdf, outl
   
def pd_pair_confusion_set_border(writer, sheet_name, outl, col_count, index_bool):
    
    formats, outf = pd_get_excel_formats(writer, )
    worksheet = writer.sheets[sheet_name]
    
    # worksheet.conditional_format(1, 1+1, 1,2+1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[1]})
    # worksheet.conditional_format(1, 0+1, 1,2+1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[1]})
    # worksheet.conditional_format(1, 0+1, 1, col_count , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[1]})
    # worksheet.conditional_format(1, 0, 1, col_count-1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[1]})
    worksheet.conditional_format(1, int(index_bool), 1, col_count-1+int(index_bool) , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[1]})
    for i in range(len(outl)-1):
        if outl[i] != outl[i+1]:
            # worksheet.conditional_format(outl[i]+1, 1+1, outl[i+1]+1-1,2+1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':outf[i]})
            # worksheet.conditional_format(outl[i]+1, 1, outl[i+1]+1-1,2 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':outf[i]})
            worksheet.conditional_format(outl[i]+1, 1+int(index_bool), outl[i+1]+1-1,2+int(index_bool) , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':outf[i]})
            
            # worksheet.conditional_format(outl[i+1]+1, 1+1, outl[i+1]+1,2+1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[0]})
            # worksheet.conditional_format(outl[i+1]+1, 0+1, outl[i+1]+1,2+1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[0]})
            # worksheet.conditional_format(outl[i+1]+1, 0+1, outl[i+1]+1,col_count , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[0]})
            # worksheet.conditional_format(outl[i+1]+1, 0, outl[i+1]+1,col_count -1 , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[0]})
            worksheet.conditional_format(outl[i+1]+1, int(index_bool), outl[i+1]+1,col_count -1 + int(index_bool) , {'type': 'cell', 'criteria':'!=', 'value':'"<None>"', 'format':formats[0]})
        
def pd_pair_confusion_to_excel(df, pair, writer, sheet_name, _round=3, base0=['Text','Intent','y_pred_0'], wrong_n=-1, same_n=10, other_n=3, rename_config={},index_bool=True):
    
    sheet_name = re.sub('['+re.escape("[]:*?/\\")+']', "", sheet_name)
    
    outdf, outl = get_pair_confusion_document(df, pair, base0, wrong_n=wrong_n, same_n=same_n, other_n=other_n)
    outdf = outdf.rename(columns=rename_config)
    pd_to_excel(outdf, writer, sheet_name, _round=_round, max_len_threshold=80,index_bool=index_bool)
    pd_pair_confusion_set_border(writer, sheet_name, outl, outdf.shape[1], index_bool=index_bool)

def pd_excel_sheet_set_column_width(worksheet, df, min_len_threshold=7, max_len_threshold=35, index_bool=True):
    df = df.reset_index()
     
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        
        if len(str(series.name)) == 0:
            width = 24
        else:
            max_len = max((series.astype(str).map(len).max(), len(str(series.name)))) + 1
            width = min(max_len, max_len_threshold)
            width = int((width-10)*0.8) + 10 if width > 10 else int(width*0.8) 
            width = max(width, min_len_threshold)

        worksheet.set_column(idx-1+int(index_bool), idx-1+int(index_bool), width)
        
def pd_to_excel(df, writer, sheet_name, _round=3, min_len_threshold=7, max_len_threshold=35, index_bool=True):
    
    sheet_name = re.sub('['+re.escape("[]:*?/\\")+']', "", sheet_name)
    
    df = df.round(_round)
    df.to_excel(writer, sheet_name=sheet_name, index=index_bool)
    worksheet = writer.sheets[sheet_name]
    
    pd_excel_sheet_set_column_width(worksheet, df, min_len_threshold=min_len_threshold, max_len_threshold=max_len_threshold, index_bool=index_bool)
    worksheet.freeze_panes(1, 0)
            

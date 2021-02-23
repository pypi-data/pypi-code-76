# %%
import pandas as pd
import numpy as np
import jsonlines

try:
    from styleframe import StyleFrame, utils
except:
    pass

# %%

################################################################
################################################################

def filter_zero(dfout):
    dfout = dfout.loc[:, (dfout != 0).any(axis=0)]
    dfout = dfout.loc[(dfout != 0).any(axis=1), :]
    return dfout

################################################################
################################################################

def get_excel_colors(excelpath):
    existing_colors = set()
    def cell_iterator_func(cell):
        existing_colors.add(cell.style.bg_color)
        return cell
    sf = StyleFrame.read_excel(excelpath, read_style=True, use_openpyxl_styles=False)
    sf = StyleFrame(sf.applymap(cell_iterator_func).dropna(axis=(0, 1), how='all'))
    return existing_colors

def read_color_filtered_excel(excelpath, color_filters=[]):
    def color_filter_func(cell):
        assert isinstance(color_filters, (list,set,dict))
        return cell if cell.style.bg_color in color_filters else np.nan
    sf = StyleFrame.read_excel(excelpath, read_style=True, use_openpyxl_styles=False)
    sf = StyleFrame(sf.applymap(color_filter_func).dropna(axis=(0, 1), how='all'))
    df = sf.data_df.applymap(lambda x: x.value)
    return df
    
################################################################
################################################################

# %%
def pdselect(df, config):
    
    if config == []:
        return df
    
    operators = {
        '>': lambda x, y: x > y, 
        '<': lambda x, y: x < y, 
        '>=': lambda x, y: x >= y, 
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y, 
        '!=': lambda x, y: x != y,  
    }
    
    df_columns = list(df.columns)
    
    _conditions = []
    
    for i in config:
        
        _operand1 = df[i[0]]
        
        if i[2] in df_columns:
            _operand2 = df[i[2]]
        else:
            _operand2 = i[2]
        
        if(i[1] in operators):
            _operator = operators[i[1]]
            _condition = _operator(_operand1, _operand2)
        else:
            _operator = _operand1
            for attr in i[1].split('.'):
                _operator = getattr(_operator, attr)
            _condition = _operator(_operand2)
        _conditions.append(_condition)
    
    pd_select_bool_vector = _conditions[0]
    for _condition in _conditions:
        pd_select_bool_vector = pd_select_bool_vector & _condition
    
    return df[pd_select_bool_vector]
    
    # pd_select(outputdf, [['Intent', 'str.contains', 'eczane'],
    #                      ['Intent-f1', '<', 0.9],
    #                      ['Intent', 'isin', ['ik_eczane']],
    #                     ])
    pass

def pddisplay(df, vertical=False, vertical_limit=-1, b=True):
    if(b):
        if not vertical:
            pd.set_option("display.max_rows", 3000)
            pd.set_option("display.max_colwidth", 300)
            display(df)
            pd.reset_option("display.max_rows")
            pd.reset_option("display.max_colwidth")
        elif vertical:
            if vertical_limit==-1:
                vertical_limit = len(df) 

            for i in range(vertical_limit):
                display(df.iloc[i:i+1].T.style.set_table_styles([
                    dict(
                        selector="td",
                        props=[("font-size","14px"), ("max-width","800px")]
                    ),
                    dict(
                        selector="tr",
                        props=[("font-size","14px"), ("max-width","800px")]
                    )
                ]))

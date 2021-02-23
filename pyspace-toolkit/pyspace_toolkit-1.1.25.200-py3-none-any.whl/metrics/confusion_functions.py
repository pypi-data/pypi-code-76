# %%
import pyspace

# %%
import numpy as np
import pandas as pd


# %%
def get_confusion_matrix(y_true, y_pred, class_count, mode = 0):
    
    if(mode == 0):
        cm = np.zeros((class_count,class_count))
        for true, pred in zip(y_true, y_pred):
            cm[true,pred] += 1
    elif(mode == 1):
        cm = np.zeros((class_count,class_count))
        for true, pred in zip(y_true, y_pred):
            cm[true,pred] += 1
            cm[pred,true] += 1
        
    return cm



# %%
def flatten_confusion(cmdf):
    
    flattened = []

    for intent_i in cmdf.index:
        for intent_j in cmdf.columns:
            if(cmdf.at[intent_i, intent_j] != 0):
                flattened.append( (intent_i, intent_j, cmdf.at[intent_i, intent_j]) )

    flatdf = pd.DataFrame(flattened, columns = ['true', 'pred', 'count'])
    flatdf = flatdf.sort_values('count', ascending=False)

    return flatdf


# %%
def extend_confusion(confusion):

    def f_key(df):
        return list(set(sum([list(df[c].values)  for c in list(df.columns)], [])))

    def f_other(sr):
        l = list(sr[['true','pred']].values)
        l.remove(intent)
        l = l[0]
        return l

    def f_conf(df, list1):
        return df[ (df['true'].isin(list1)) | (df['pred'].isin(list1))]

    def f_conf_2(df, list1):
        return df[ (df['true'].isin(list1)) & (df['pred'].isin(list1))]


    result = []

    confused_intents = f_key(confusion[['pred', 'true']])
    for intent in confused_intents:

        _p = f_conf(confusion, [intent])

        for _, i in _p.iterrows():

            _mislabel = f_other(i)

            _r = f_conf(confusion, [_mislabel])
            _u = f_conf(confusion, [intent, _mislabel])
            _i = f_conf_2(confusion, [intent, _mislabel])


            __p = _p['count'].sum()
            __r = _r['count'].sum()
            __u = _u['count'].sum()
            __i = _i['count'].sum()


            __i_to_m = _i[(_i['true'] == intent) & (_i['pred'] == _mislabel)]['count'].values
            __m_to_i = _i[(_i['true'] == _mislabel) & (_i['pred'] == intent)]['count'].values

            __i_to_m = 0 if len(__i_to_m) == 0 else __i_to_m[0]
            __m_to_i = 0 if len(__m_to_i) == 0 else __m_to_i[0]

            result.append((intent, __p, _mislabel, __r, __i, __i_to_m, __m_to_i, __u, __i/__p, __i/__r, __i/__u))

    resdf = pd.DataFrame(result,
         columns=['true', '<t>', 'pred', '<p>', '<i>', '<tp>', '<pt>', '<u>', '<i/t>', '<i/p>', '<i/u>']
        ).drop_duplicates().reset_index(drop=True)
    resdf = resdf[['true', 'pred', '<tp>', '<pt>', '<i>', '<t>', '<p>', '<u>', '<i/t>', '<i/p>', '<i/u>']]
    resdf = resdf.rename(columns={'<tp>': 'count', '<pt>': 'reverse count'})
    resdf = resdf.rename(columns={'reverse count': 'r. count'})
    
    # resdf.sort_values(['count', 'r. count'], ascending=False)
    # resdf.sort_values(['<i/u>', 'count', 'r. count'], ascending=False)
    # resdf.sort_values(['<i/u>', '<i>'], ascending=False)
    # resdf = resdf.sort_values(['<i>', '<i/u>'], ascending=False)
    # resdf = resdf.sort_values(['<i/t>', '<i>', '<i/u>'], ascending=False)
    
    resdf['sort'] = resdf.apply(lambda x: x['<i>']*np.sqrt(x['<i/t>']) + int(bool((x['<i>'] - 1 )))*10, axis=1 )
    resdf = resdf.sort_values(['sort'], ascending=False).drop(columns=['sort'])
    
    return resdf


# %%
def get_confusion_analysis(y_true, y_pred, labelencoder):
    
    cm = get_confusion_matrix(y_true,y_pred, len(labelencoder.classes_))
    cmdf = pd.DataFrame(cm, index=labelencoder.classes_, columns=labelencoder.classes_)
    np.fill_diagonal(cmdf.values, 0)
    cmdf = pyspace.pandas.pdfunctions.filter_zero(cmdf)

    flatdf = flatten_confusion(cmdf)
    
    confusion = extend_confusion(flatdf)
    
    return confusion

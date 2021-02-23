# %%
import sklearn
from sklearn import metrics

import pandas as pd


# %%
def get_scores(y_true, y_pred):
    
    result = {}
    
    config = {'acc':{}, 'f1':['weighted','macro',]}
    
    name_prefix_length = 12
    
    if 'acc' in config:
        name = 'accuracy'
        name = name + ' '*(name_prefix_length - len(name))
        result[name] = sklearn.metrics.accuracy_score(y_true, y_pred )
        print(name+' :',result[name])
        
    if 'f1' in config:
        for average in config['f1']:
            name = 'f1 ' + average
            name = name + ' '*(name_prefix_length - len(name))
            result[name] = sklearn.metrics.f1_score(y_true, y_pred, average=average )
            print(name+' :',result[name])
            
    return result


# %%
def get_report(y_true, y_pred, le=None, vc=None, mode=0):
    if le:
        target_names = set(y_pred).union(set(y_true))
        target_names = [le.classes_[lid] for lid in target_names]
    else:
        target_names = None

    if str(type(vc)) != str(type(None)):
        for i in list(set(y_pred)):
            if i not in vc:
                vc[i] = 0
        
    if mode in [0,1]:
        c_report = sklearn.metrics.classification_report(y_true, y_pred , target_names=target_names, output_dict=True)

        templist = []
        for c in c_report:
            if(c in ['accuracy', 'macro avg', 'weighted avg']):
                continue
                
            if str(type(vc)) == str(type(None)):
                templist.append((c, c_report[c]['precision'], c_report[c]['recall'], c_report[c]['f1-score'], c_report[c]['support']))
            else:
                templist.append((c, c_report[c]['precision'], c_report[c]['recall'], c_report[c]['f1-score'], c_report[c]['support'], vc[c]))
                
        if str(type(vc)) == str(type(None)):
            tempdf = pd.DataFrame(templist,columns=['i', 'precision', 'recall','f1', 'test count'])
        else:
            tempdf = pd.DataFrame(templist,columns=['i', 'precision', 'recall','f1', 'test count', 'train count'])
            
        tempdf = tempdf.sort_values(['f1'],ascending=False).reset_index(drop=True)
        
        if mode == 0:
            return tempdf
            
        elif mode == 1:
            
            if str(type(vc)) == str(type(None)):
                print(" "*50, '', " "*len(" : "), "precision", " "*2, "recall", " "*2, "f1-score", " "*3, "test count")
            
            else:
                print(" "*50, '', " "*len(" : "), "precision", " "*2, "recall", " "*2, "f1-score", " "*3, "train count", " "*3, "test count")
            print()
            for xx, row in tempdf.iterrows():
                c = row['i']

                if(c in ['accuracy', 'macro avg', 'weighted avg']):
                    continue
                p = str(round(c_report[c]['precision'], 3))
                p = p + "0"*(5-len(p))
                r = str(round(c_report[c]['recall'], 3))
                r = r + "0"*(5-len(r))
                f = str(round(c_report[c]['f1-score'], 3))
                f = f + "0"*(5-len(f))
                sp = c_report[c]['support']
                
                
                if str(type(vc)) == str(type(None)):
                    print(c, " "*(50-len(c)), ' : ', p, ' '*(11-len(str(p))), r, ' '*(8-len(str(r))), f, ' '*(11-len(str(f))), sp )
                else:
                    vci = vc[c]
                    print(c, " "*(50-len(c)), ' : ', p, ' '*(11-len(str(p))), r, ' '*(8-len(str(r))), f, ' '*(11-len(str(f))), vci,' '*(14-len(str(vci))), sp )
                    
    elif mode == 2:
        print(sklearn.metrics.classification_report(y_true, y_pred , target_names=target_names))


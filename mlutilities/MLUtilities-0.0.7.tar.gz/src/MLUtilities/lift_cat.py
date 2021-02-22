import pandas as pd

""" 
This function calculates the lift ratio for a binary
target label.

"""


def lift_cat(Data,feature,target):
    '''
     This functions calculates the lift ratio for a given categorical feature

    '''
  
    d1=Data[[feature,target]][Data[target]==1].groupby([feature]).count().sort_values(target, ascending=False)
    Data=Data[[feature,target]][Data[target]==0].groupby([feature]).count().sort_values(target, ascending=False)
    den_d1=d1[target].sum()
    den_Data=Data[target].sum()
    Data['Clean_percent']  = (Data[target]/den_Data)*100
    d1['target_percent']  = (d1[target]/den_d1)*100
    d3 = pd.merge(d1, Data, how='inner', on=[feature])
    d3.rename(columns={'f_x': 'target_Count'}, inplace=True)
    d3.rename(columns={'f_y': 'Clean_Count'}, inplace=True)
    d3['Lift_Ratio']  =  d3.target_percent/d3.Clean_percent
    d3.sort_values('Lift_Ratio', ascending=False, inplace=True)
    d3 =d3.reset_index()
    d3.rename(columns={feature: 'Category_levels'}, inplace=True)
    d3['feature_name'] =feature
    #d3= pd.concat([d3],axis=1)
    #move feature_name column from back to front column
    col = d3.pop("feature_name")
    d3.insert(0, 'feature_name', col)
    return d3
    
    
    
def mult_lift(Data,columns,target):
    df=[]
    for name in columns:
        df.append(lift_cat(Data,name,target))
        df2 = pd.concat(df)
    return df2    
import pandas as pd

def lift_boolean (lift_threshold,lift_df,actual_df):
    '''
     This function creates a boolean feature   for a given categorical feature
     by selecting those category levels that provide the highest lift ratio.
     The lift ratio is calculated by dividing the percent of fraud transactions by the
     percent of clean transactions.
     It appends the new boolean feature to the old dataframe that was given as the input
     to the function.
    '''
    lift_df = lift_df[lift_df.Lift_Ratio > lift_threshold ]    
    cols =   lift_df.feature_name.unique()
    cols_2 = list(set(actual_df.columns) & set(cols))
    for i in cols_2:
    #create a boolean column in Data  if the  column i  elements are in the lift category list
        actual_df['Bool_'+ i]= [1 if actual_df[i].values.tolist()[j] in lift_df.Category_levels.to_list() else 0 for j in range(actual_df.shape[0])]
        #Counter(Data['Bool_'+ i])
    return actual_df
	
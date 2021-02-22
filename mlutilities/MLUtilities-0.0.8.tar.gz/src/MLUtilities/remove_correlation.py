import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency

def remove_correlation(data, threshold):
    ''' 
    Find correlation among columns of a dataframe
    return names of columns removed  
    return  reduced dataframe with correlated columns removed
    '''
# Create correlation matrix
    corr_matrix = data.corr().abs()

# Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

# Find features with correlation greater than 0.95
    drop_columns = [column for column in upper.columns if any(upper[column] > threshold)]

# Drop features 
    red_data=data.drop(drop_columns, axis=1)
    print('Features Removed : {}'.format(drop_columns))
    #sys.stdout.write('Features Removed : {}'.format(drop_columns))

    return  drop_columns, red_data
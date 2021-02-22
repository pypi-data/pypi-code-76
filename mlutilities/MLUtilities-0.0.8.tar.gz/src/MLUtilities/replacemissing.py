def replacemissing(data):
    ''' This function takes a dataframe as input ,replaces missing values for categorical features with
     -9999.01 and for the numeric columns, the median of the column.

    '''
    categorical_cols = [x for x in data.columns if data[x].dtypes  in ['object']]
    numeric_cols = [x for x in data.columns if data[x].dtypes  in ['int64','float64']]
    data[categorical_cols].fillna(-9999.01,inplace=True)
    data[numeric_cols] = data[numeric_cols].apply(lambda x: x.fillna(x.median()),axis=0)
    return data
import pandas as pd


def get_value_counts_with_expansion_factor(
    df_, counted_cols, factor_column, normalize=True, dropna=True):
    '''
    Analogue to Series.value_counts but aplifiying rows by an expansion 
    factor column.
    
    Parameters
    ----------
    df : DataFrame,
        where expanded value counts will be performed.
    counted_cols : str or list of str
        column name(s) of column(s) to be counted.
    factor_column : str,
        column name specifying where the expansion factor of each row 
        should be found.
    '''
    
    if not isinstance(counted_cols, list):
        
        counted_cols = [counted_cols] 
                
        
    df = df_[counted_cols + [factor_column]].copy()
    
    if (not dropna) and (df[counted_cols].select_dtypes('category').shape[1] == 0):
        df[counted_cols] = df[counted_cols].fillna('NA')

    
    expanded_value_counts = df.groupby(counted_cols)[factor_column].sum()
    
    if normalize:
        expanded_value_counts = \
            expanded_value_counts / expanded_value_counts.sum()
        
    return expanded_value_counts

def get_percentage_table_with_expansion_factor(df, counted_col, factor_column,
                                               dropna=True):
    '''
    Analogue to Series.value_counts but aplifiying rows by an expansion 
    factor column, but additionally concatenates percentage column(s).
    
    Parameters
    ----------
    df : DataFrame,
        where expanded value counts will be performed.
    counted_cols : str or list of str
        column name(s) of column(s) to be counted.
    factor_column : str,
        column name specifying where the expansion factor of each row 
        should be found.
    '''
    
    sum_srs = get_value_counts_with_expansion_factor(
        df, counted_col, factor_column, normalize=False, dropna=dropna
        ).sort_index()
    sum_srs.name = 'exp_count'
    
    perc_srs = 100 * sum_srs / sum_srs.sum()
    perc_srs.name = 'percentage'
    perc_df = pd.concat([sum_srs, perc_srs], axis=1)

    # get percentage for the union of all levels except the last one 
    # which is already calculated 
    if isinstance(counted_col, list):
        
        union_str = '_U_'
        level_str = 'L'
        
        for l in range(len(counted_col) - 1, 0, -1):
            
            # initialize column which will contain Union(range(i)) 
            # percentage
            colname_ = union_str.join(
                [f"{level_str}{i}" for i in range(l)]) + '_percentage'
            perc_df.loc[:, colname_] = perc_df.percentage
            
            # get percentage subtotal on levels range(l)
            subtotals_srs = perc_df.groupby(level=list(range(l)))[
                'percentage'].sum()
            
            for idx, val in subtotals_srs.iteritems():
                
                # calculate Union(range(i)) percentage
                perc_df.loc[idx, colname_] = (100 * perc_df['percentage'].loc[
                    idx] / val).values
        
        # rename percentage column
        colname_ = union_str.join(
            [f"{level_str}{i}" for i in range(len(counted_col))]) +\
            '_percentage'
        perc_df = perc_df.rename(columns={'percentage': colname_})

    
    return perc_df


def get_weighted_average(df, col_to_average, weight_col):
    '''
    Computes the weighted average of pandas column using weitghts from
    another column

    Parameters
    ----------
    df : DataFrame,
        where columns are stored.
    col_to_average : hashable,
        points to the column from which the average is computed
    weight_col : hashable,
        point to the column where weights are extracted
    '''
    
    numerator = df[col_to_average] * df[weight_col]
    denominator = df[weight_col].sum()
    
    unpacked_division = numerator / denominator
    
    return unpacked_division.sum()

# ftp_cleanse.py
# Dependencies: pandas

import pandas as pd


def ftp_cleanse_file(ftp_df):
    """
    -------------------------------------------------------
    Fills a dataframe with dummy values in each of the
    columns of which the original dataframe had data in.
    The resulting dataframe will only contain one row.
    -------------------------------------------------------
    Parameters:
        ftp_df : pandas.DataFrame
            DataFrame with data that will be cleansed.
            All columns filled in this dataframe will be
            replaced with dummy values in the returned DF.
    Returns:
       dummy_df : pandas.DataFrame
            Dummy DataFrame containing only one row, of
            dummy values filled in the same columns as
            those that were filled in the original DF.
    ------------------------------------------------------
    """

    dummy_fill_val = "AAAAAAAAAAAAAAAAA"

    # Create a copy of the downloaded dataframe
    dummy_df = ftp_df.copy()

    # Remove all but the first row in downloaded dataframe
    dummy_df = dummy_df.iloc[:1]

    # Find which columns are filled and which are not
    filled_cols = []
    for col in dummy_df.columns:
        isFilled = not dummy_df[col].isna().any()
        filled_cols.append(isFilled)

    # Replace all filled columns with dummy value
    index_counter = 0

    for isFilled in filled_cols:
        if isFilled:
            dummy_df[dummy_df.columns[index_counter]] = [dummy_fill_val]
        index_counter += 1

    # Upload the dummy value, returning the result of upload
    return dummy_df

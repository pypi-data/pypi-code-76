import pandas as pd
import boto3


def load_survey_data(path, load_func,
                     columnnames_to_lower=True,
                     ) -> pd.DataFrame:
    """
    Loads survey DataFrame locally

    Parameters
    ----------
    path : str or pathlib.Path,
        dataframe filename.
    columnnames_to_lower : bool,
        specifies if column names need to be converted to lower.
    load_func : callable,
        it's unique argument needs to be `path`.
    """
    survey_hp = load_func(path)

    if columnnames_to_lower:
        survey_hp.columns = survey_hp.columns.str.lower()

    return survey_hp


def load_s3_data(profile_name,
                 bucket_name,
                 key,
                 load_func,
                 columnnames_to_lower=True):
    """
    Loads data DataFrame from s3 bucket

    Parameters
    ----------
    profile_name : str ,
        AWS profile name.
    bucket_name : str ,
        AWS bucket name.
    key : str,
        AWS key to be used on bucket to find the target file
    columnnames_to_lower : bool,
        specifies if column names need to be converted to lower.
    load_func : callable,
        it's unique argument needs to be `path`.
    """
    # instance s3 connection
    boto3.setup_default_session(profile_name=profile_name)
    s3 = boto3.client('s3')

    # read file
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    ar_df = load_func(obj)

    if columnnames_to_lower:
        ar_df.columns = ar_df.columns.str.lower()

    return ar_df
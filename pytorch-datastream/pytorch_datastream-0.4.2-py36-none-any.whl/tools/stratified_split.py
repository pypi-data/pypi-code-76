import warnings
from typing import Dict, Optional
from pathlib import Path
from datastream import tools


def stratified_split(
    dataset,
    key_column ,
    proportions  ,
    stratify_column  = None,
    filepath  = None,
    seed  = None,
    frozen  = False,
):
    if (
        stratify_column is not None
        and any(dataset.dataframe[key_column].duplicated())
    ):
        
        warnings.warn(
            'Trying to do stratified split with non-unique key column'
            ' - cannot guarantee correct splitting of key values.'
        )
    strata = {
        stratum_value: dataset.subset(
            lambda df: df[stratify_column] == stratum_value
        )
        for stratum_value in dataset.dataframe[stratify_column].unique()
    }
    split_strata = [
        tools.unstratified_split(
            stratum,
            key_column=key_column,
            proportions=proportions,
            filepath=filepath,
            seed=seed,
            frozen=frozen,
        )
        for stratum_value, stratum in strata.items()
    ]
    return {
        split_name: type(dataset).concat(
            [split_stratum[split_name] for split_stratum in split_strata]
        )
        for split_name in proportions.keys()
    }

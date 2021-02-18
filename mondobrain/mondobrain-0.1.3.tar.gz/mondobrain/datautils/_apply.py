from typing import Dict, List, Union

import numpy as np
import pandas as pd


def _condition_mask(s: pd.Series, cond: Union[dict, str]):
    if isinstance(cond, dict):
        lo, hi = cond["lo"], cond["hi"]
        return (s >= lo) & (s <= hi)

    return s == cond


def conditions_mask(df: pd.DataFrame, rule: dict):
    """ Get a mask based on a dictionary of conditions
    """
    masks = []
    for key, cond in rule.items():
        masks.append(_condition_mask(df[key], cond))

    return np.all(np.array(masks), axis=0)


def apply_rule(df: pd.DataFrame, rule: dict, inverse: bool = False) -> pd.DataFrame:
    """ Applies the rule to the population df to obtain a sample

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to apply the rule to

    rule : dict
        A set of conditions to apply to the dataframe

    inverse : boolean, default=False
        If True, the inverse of the rule is applied

    Returns
    -------
    sample: pd.DataFrame
        The sample of the original dataframe based on rule conditions
    """
    if not rule:
        raise ValueError("An empty rule cannot be applied to a dataframe")

    mask = conditions_mask(df, rule)

    if inverse:
        mask = ~mask

    return df[mask]


def apply_rules(
    df: pd.DataFrame, rules: List[Dict], inverse: bool = False, operation: str = "or"
) -> pd.DataFrame:
    mask = [conditions_mask(df, rule) for rule in rules if rule]

    if len(mask) == 0:
        raise ValueError("No rule found to apply to the dataframe")

    if operation == "or":
        mask = np.any(mask, axis=0)
    elif operation == "and":
        mask = np.all(mask, axis=0)
    else:
        raise ValueError("operation type not supported")

    if inverse:
        mask = ~mask

    return df[mask]

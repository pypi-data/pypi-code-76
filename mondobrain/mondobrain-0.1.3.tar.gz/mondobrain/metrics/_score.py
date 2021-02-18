from category_encoders import OrdinalEncoder
import numpy as np
import pandas as pd

from mondobrain.datautils import apply_rule
from mondobrain.utils.data import is_continuous

from ._target import target_metrics


def score(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    rule: dict = None,
    population: pd.DataFrame = None,
):
    """Score a dataframe

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. If rule is set, then df should represent the original
        population. If population is set, then df should represent the sample to score.

    outcome : str, default=None
        Which column to use as the outcome for the score (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    rule: dict, default=None
        The solver rule to use for scoring. This or population must be set, but not
        both. If set, df should be the population dataset

    population: pd.DataFrame, default=None
        The population dataset to base the score off of. If set, df should be the sample
        dataset.

    Returns
    -------
    score: float
        The score of the sample and population
    """
    # Quick checks to make sure that one of rule and population is set.
    if rule is None and population is None:
        raise ValueError("one of `rule` or `population` must be set")

    if rule is not None and population is not None:
        raise ValueError("only one of `rule` or `population` may be set")

    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        target = df[outcome].iloc[0] if df[outcome].dtype == np.object else "max"

    if population is not None:
        sample = df

    if rule is not None:
        population = df
        sample = apply_rule(df, rule)

    # Encode our outcome column if the outcome column is continuous
    if is_continuous(population[outcome].dtype):
        enc = OrdinalEncoder(cols=[outcome], handle_missing="return_nan")
        population = enc.fit_transform(population)
        sample = enc.transform(sample)

    # Get metrics for population and sample
    pop_metrics = target_metrics(population[outcome], target)
    smp_metrics = target_metrics(sample[outcome], target)

    # Return 0 if we our size is 0
    if smp_metrics["size"] == 0 or pop_metrics["size"] == 0:
        return 0

    return (
        np.sqrt(smp_metrics["size"])
        * (smp_metrics["mean"] - pop_metrics["mean"])
        / pop_metrics["std"]
    )

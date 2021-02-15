import pandas as pd
import numpy as np
import warnings

def get_weighted_complete_randomization_series_on_subset(
        weight_srs, subset_bool_srs, success_determinant, how='prob', errors='warn', seed=300):
    """
    NOTE: when this function was implemented in COVID Brasil, it didn't
    work. It should be considered EXPERIMENTAL.
    Get complete randomization series of 0 and 1 on a subset a Series.
    Observations out of the subset will take 0 as default value.

    Parameters
    ----------
    weight_srs : Series,
        Contains the weights of each observation. It's index will be
        used in the returned series.
    subset_bool_srs: Series of bool,
        Specifies the columns where weights should be considered for the
        randomization procedure.
    success_determinant : float,
        Sets the probability or the sum of success in the complete
        randomization procedure according to `how`.
    how : str in {'prob', 'sum'},
        Indicates if `success_determinant` corresponds to a probability
        of success or to the total number of successes. Defaults to
        'prob'.
    errors: str in {'warn'}, #\todo add other behaviors
        Indicates how the error of having a  number of successes grater
         than the subset population should behave. Defaults to 'warn'.
    seed : random seed,
        Used as argument of `np.random.seed` for ensuring replicability`.

    Returns
    -------
    Series indexed as `weight_srs`, containing zeros and ones, after
    complete randomization made on the subset defined by `subset_bool_srs`.
    Observations out of the subset will take 0 as default value.

    Example
    -------
    To get the income after a shock defined by a `job_loss_probability`
    on a DataFrame `df` containg weights on column 'weight', income on
    column 'income', and having a boolean series for specifying the rows
    which belong to a specific economic sector in `sector_bools`, the
    output of this function could be used as follows:
    >>>df['income'] * (
    ...    1 - get_weighted_complete_randomization_series_on_subset(
    ...        df['weights'], sector_bools, job_loss_probability))
    """
    warnings.warn(
        "when this function was implemented in COVID Brasil, it didn't"
        "work. It should be considered EXPERIMENTAL.",
        DeprecationWarning, stacklevel=2)
    assert how in ['prob', 'sum'], "`how` must takes values in ['prob', 'sum']"

    # shuffle observations
    np.random.seed(seed)
    shuffled_weights = weight_srs[subset_bool_srs].sample(frac=1)

    # get cumulated sum of weights
    cumsum_weights = shuffled_weights.cumsum()

    # get sum of weights of select observations
    if how == 'prob':
        sum_weights_selected = cumsum_weights.iloc[-1] * success_determinant
    elif how == 'sum':
        sum_weights_selected = success_determinant

    # check if numbers of successes is smaller than subset popuation
    if sum_weights_selected > cumsum_weights.iloc[-1]:
        if errors == 'warn':
            warnings.warn(
                "The number of successes is grater than the subset"\
                "population",
                RuntimeWarning, stacklevel=2)
        # \todo other cases

    # get index of succeded observations
    succeeded_index = cumsum_weights.index[
        cumsum_weights < sum_weights_selected]
    print(len(succeeded_index))

    # build randomization vector
    randomization_srs = pd.Series(np.zeros_like(weight_srs),
                                  index=weight_srs.index)
    randomization_srs.loc[succeeded_index] = 1

    return randomization_srs


def copy_docstring(sender):
    """Decorator for copying docstrings among functions.

    Parameters
    ----------
    sender: callable,
        where docstring will be copied from.
    receiver: callable,
        where dostring will be copied to.

    Example
    -------
    It can be used for different loader functions defined in each
    country source folder, normally in `utils.dataload`, by building
    wrappers of the agnostic functions defined in `covidsource.utils.
    dataload`.
    In the following example `sender=load_survey_data` and `receiver=
    load_survey_data_sv`:
    >>>@copy_docstring(load_survey_data)
    ...def load_survey_data_sv(path=SURVEY_DATA_PATH,
    ...                        load_func=LOCAL_LOAD_FUNC,
    ...                        columnnames_to_lower=True,
    ...                       ) -> pd.DataFrame:
    ...    return load_survey_data(
    ...        path, load_func,
    ...        columnnames_to_lower=columnnames_to_lower)

    source: https://softwareengineering.stackexchange.com/questions/
    386755/sharing-docstrings-between-similar-functions
    """

    def wrapper(receiver):
        receiver.__doc__ = sender.__doc__
        return receiver
    return wrapper


def bernoulli_on_rows(srs, row_bools, prob, seed = 300):
    '''Set values to zero using Bernoulli distribution on specific rows 
    of a Series.
    
    Parameters
    ----------
    srs : Series, 
        Series where specific rows are set as zero with probability `prob`.
    rows_bools: Series of bool
        specifies the columns where the values should be set to zero with
        probability `prob`.
    prob : float, 
        governs Bernoulli distribution.
    seed : random seed,
        used as argument of `np.random.seed` for ensuring replicability`.
    '''
    
    # generate bernoulli sample 
    np.random.seed(seed)
    bernoulli_srs = pd.Series(np.random.binomial(n = 1, p = prob, size =len(srs)))
    
    # exclude rows
    bernoulli_srs.loc[~ row_bools] = 1
    output = srs * bernoulli_srs.values
    
    return output
    

def uniform_decay(df, col, row_bools, decay):
    '''Apply uniform decay on column for specific rows. 
    
    Parameters
    ----------
    col : str,
        defines which is the column where this decay is applied.
    row_bools : Series of bool,
        define wich are the rows of `col` where uniform decay is  
        applied.
    decay : float,
        selected rows from `col` are multiplied by (1 - `decay`).
    '''
    unif_decay = row_bools.astype(float)
    unif_decay = unif_decay.replace(1, 1 - decay).replace(0, 1)
    output = df[col] * unif_decay
    return output
    

def proportional_cut(X, continuous_feature, threshold_col, n_buckets_threshold,
                     n_buckets_total, collapse_negative=False, **cut_kwargs):
    """
    Transform continuous feature in binarized buckets proportional to a
    selected threshold.

    Parameters
    ----------
    X : pd.DataFrame,
        Where columns are extracted.
    continuous_feature : column label,
        Indicates which column will be binarized.
    threshold_col : column label,
        Indicates which column is used as threshold.
    n_buckets_threshold : int,
        number of bins to be used to reach threshold.
    n_buckets_total: int,
        total number of buckets. The rightmost bin will be unbounded,
        i.e. will contain which are greater than the seond last bin.
    collapse_negative : bool,
        whether negative values should be assigned to the leftmost bin.
        Default `False` (recommended).
    cut_kwargs : kwargs
        Keyword arguments to be used in pd.cut function.
    """

    bins = [i / n_buckets_threshold for i in range(0, n_buckets_total)]
    bins.append(np.inf)

    if collapse_negative:
        X.loc[X[continuous_feature] < 0, continuous_feature] = 0

    return pd.cut(
        X[continuous_feature] / X[threshold_col],
        bins=bins,
        labels=[i + 1 for i in range(n_buckets_total)],
        **cut_kwargs
    )


def weighted_qcut(X, to_order_col, weights_col, q, **kwargs):
    """Return weighted quantile cuts from a given series, values.

    Parameters
    ----------
    X : pd.DataFrame,
        contains `to_order_col` and `weights_col`.
    to_order_col : column label,
        indicates the column according to which rows have to be ordered.
    weights_col : column label,
        indicates the column of weights.
    q : int,
        number of bins.
    """
    from pandas._libs.lib import is_integer

    if is_integer(q):
        quantiles = np.linspace(0, 1, q + 1)
    else:
        quantiles = q

    ordered_cum_sum = X[weights_col].iloc[X[to_order_col].argsort()].cumsum()
    bins = pd.cut(ordered_cum_sum / ordered_cum_sum.iloc[-1], quantiles,
                  **kwargs)
    return bins.sort_index()


def get_partition_bool_columns_dict(
        bool_cols, more_than_once, none_default, prefix='Solo ',
        suffix_to_remove='first'):
    """
    Returns dict to be used as `select_map` dict value on a
    `SelectTransformer` to partition a set of columns.

    The resulting partition first option will be two or more bool
    conditions from `bool_cols` followed by one per each bool column
    from `bool_cols` and if any bool condition is met from `bool_cols`,
    the default value will be used.

    Parameters
    ----------
    bool_cols : iterable of str,
        contains labels of columns where program `bool` observations
        will indicate whether or not the household is beneficiary of the
        program.
    more_than_once: str,
        used as choice when more than one bool condition is met on a
        row.
    none_default : str,
        used as default choice when no condition is met.
    prefix : str (optional),
        used as prefix on every choice which correspond to a single
        bool column from `bool_cols`. Default `'Solo '`
    suffix_to_remove : str (optional),
        to be removed from program cols on `choicelist`. Default
        `'first'`.
    """

    conditions = [
        lambda df, bool_cols=bool_cols:(df[bool_cols].sum(1) >= 2),
        * [(lambda df, col=col: df[col] == 1) for col in bool_cols
           ]]

    choices = [more_than_once, *[
        f'{prefix}{chn.replace(suffix_to_remove, "").replace("_", " ").strip()}'
        for chn in bool_cols
    ]]

    return {**dict(zip(choices, conditions)), **{'default': none_default}}


def new_poverty(original_poverty, modified_poverty):
    """
    Hardcoded function for getting `select_map` dict-value for computing
    new poverty.

    Parameters
    ----------
    original_poverty : column label,
        indicating the column of bools where reference poverty status
        needs to be taken.
    modified_poverty : column label,
        indicating column of bools where target poverty status  needs to
        be taken.
    """
    return {
        "Pobreza por COVID-19": lambda df, original_poverty=original_poverty,
        modified_poverty=modified_poverty: \
        (~ df[original_poverty]) & df[modified_poverty],
        "Se mantiene en pobreza": lambda df,
        original_poverty=original_poverty, modified_poverty=modified_poverty:
        df[original_poverty] & df[modified_poverty],
        "Se mantiene en no pobreza": lambda df,
        original_poverty=original_poverty, modified_poverty=modified_poverty:
        (~ df[original_poverty]) & (~ df[modified_poverty])
    }

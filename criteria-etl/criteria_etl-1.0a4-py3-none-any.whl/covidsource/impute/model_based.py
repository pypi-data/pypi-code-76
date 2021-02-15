import pandas as pd
import numpy as np
import warnings
import textwrap
from collections import defaultdict
from IPython.display import display
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression


class EstimatorFactory:
    """
    Defines how estimators should be built when imputation is based on
    predicting probabilities acccording to a model.

    Attributes
    ----------
    X_cols : list of column labels
        Indicates which subset of columns should be used as independent
        variables when defining an estimator.
    y_col : column label
        Indicates which column should bw used as dependent variable when
        defining an estimator.
    hyperparameter_determinant : dict or str in ['grid', 'random']
        If a dictionary is used, the estimator will be obtained by
        setting its parameters through it. If 'grid' or 'random' a
        search of hyperparameters will be done though grid or random
        search respectively. Defaults to `{}`.
    hyperparameter_search_kwargs : dict
        If `hyperparameter_determinant` is a dict, it will be ignored.
        If `hyperparameter_determinant` is 'grid' or 'random', it will
        be used as kwargs for `GridSearchCV` and `RandomizedSearchCV`
        objects, respectively. Defaults to `{}`.
    test_size : float
        Should be between 0.0 and 1.0 and represent the proportion of
        the dataset to include in the test split. If set to 0, no test
        set will be used. Defaults to .2.
    seed : int
        Used as random state for all the obtained estimators. Defaults
        to `6202`.
    """
    implemented_algorithms = ['lasso']
    implemented_hyperparameter_search_schemes = ['grid', 'random']

    def __init__(
            self, X_cols, y_col, algorithm='lasso',
            hyperparameter_determinant={},
            hyperparameter_search_kwargs={}, test_size=.2, seed=6202):
        # define independent and dependent variables of the estimator
        self.X_cols = X_cols
        self.y_col = y_col

        # define the algorithm which will be used to generate score
        # probabilities
        assert algorithm in self.implemented_algorithms, \
            f"{algorithm} must take values in {self.implemented_algorithms}"
        self.algorithm = algorithm
        self.hyperparameter_determinant = hyperparameter_determinant
        self.hyperparameter_search_kwargs = hyperparameter_search_kwargs
        self.test_size = test_size

        # ensure replicability
        self.seed = seed

    def get_estimator(self, df, return_test_index=False):
        """
        Returns an estimator trained on `df`. The estimator is built according
        to all `EstimatorFactory` attributes.

        Parameters
        ----------
        df : DataFrame
            Must contain all columns defined on `X_cols` and `y_col`
            attributes.
        return_test_index : bool
            Whether test index should be returned as second positional
            output. If `test_size` attribute is zero, `None` will be
            returned. Defaults to `False`.
        """
        # define estimator
        if self.algorithm == 'lasso':
            estimator = LogisticRegression(
                penalty="l1", solver="liblinear", random_state=self.seed)

        # parse `hyperparameter_determinant`
        if isinstance(self.hyperparameter_determinant, dict):
            # use `hyperparameter_determinant` as parameters of the estimator
            estimator = estimator.set_params(self.hyperparameter_determinant)

        else:
            # define hyperparameter search prcedure
            assert self.hyperparameter_determinant in \
                   self.implemented_hyperparameter_search_schemes, \
                "`hyperparameter_determinant` must take values in " + \
                f"{self.implemented_hyperparameter_search_schemes}"

            hyperparameter_search_scheme = GridSearchCV if \
                self.hyperparameter_determinant == 'grid' else \
                RandomizedSearchCV

            estimator = hyperparameter_search_scheme(
                estimator, **self.hyperparameter_search_kwargs)

        # parse fit parameters
        missing_cols = pd.Index(self.X_cols + [self.y_col]).difference(
            df.columns)
        assert len(missing_cols) == 0, \
            f"The following columns must be present on `df`:\n{missing_cols}"

        # get train and test index
        index_values = df.index.unique()
        if self.test_size > 0:
            n_samples_test = int(round(len(index_values) * self.test_size))
            np.random.seed(self.seed)
            test_index = np.random.choice(index_values, n_samples_test)
            train_index = np.setdiff1d(index_values, test_index)
        else:
            test_index = None
            train_index = index_values

        # get X and y
        X = df.loc[train_index, self.X_cols].values
        y = df.loc[train_index, self.y_col].values

        if not return_test_index:
            return estimator.fit(X, y)
        else:
            return estimator.fit(X, y), test_index


class ScoreBasedStratifiedImputer(BaseEstimator, TransformerMixin):
    """
    Inputs values on a column according to a score, a stratification
    and a desired amount of imputed values per strata.

    Attributes
    ----------
    target_col : column label
        Indicates the column where values should be imputed. It is also
        used for counting the number of observations which have already
        present values in case `objective` is set to 'deficit'. If
        `objective` is set to 'target', then the values of this column
        could be used if the `index.names` of `imputation_target_srs` 
        are a subset of `strata_cols`. 
    candidate_col : column label
        Indicates the column containing the potential values to be 
        imputed.
    score_col : column label
        Indicates the column where the score is present. Bigger scores
        will be prioritized.
    strata_cols : list of column labels
        Indicates which are the columns defining each strata.
    imputation_target_srs : Series
        Defines the number of observations to attain after the
        imputation. It must share at least one level of its 
        `index.names` with the column labels present on `strata_cols`. 
        If its ``index.names`` is a subset of `strata_cols`, an 
        inference of the distribution of the imputation target across
        strata non specified in `imputation_target_srs` will be done 
        using the distribution of `target_col` across these strata. If 
        its `index.names` are the same as defined in `strata_cols`, no 
        inference will be done.
    objective : str in {'deficit', 'target'}
        Indicates if the imputation should fill the deficit of
        `target_col`, in case it is set to 'deficit'; or impute as much 
        values as defined on `imputation_target_srs`, in case objective
        is set to 'target'.
    imputable_col : column label or None (optional)
        If column label it points to a boolean column which determines
        if an observation is imputable or not. If None, all observations
        are assumed to be imputable. Defaults to
    weight_col : column label or None (optional)
        Indicates the column to be used as expansion factor. The 
        imputed number of observations will be expanded according to 
        this column. If None, the imputed number of observations will 
        not be expanded. Defaults to None.
    transfer_strategy: list of ('index_label', {transfer_src: transfer_dst})
        (optional)
        Defines the procedure of transferring missing imputations from a
        source to a destination strata. The process is done iteratively
        respecting the order of the list and the dictionaries. Defaults
        to None.
    verbose : bool
        If some control flow checks need to be reported. Defaults to False.
    copy: bool
        Whether to copy impute on `transform` method. Will default to
        True and this option is recommended if no memory savings need to
        be made. Defaults to True.
    force : bool
        Whether or not force imputation in case of unfeasible imputation
        target. Defaults to False
    debug : bool
        If True, `debug_dict` will store the most bug prone subproducts
        of the main class methods.

    Returns
    -------
    Dataframe with a new column named `f'imputed_{target_col}'`
    containing an imputed copy of `target_col`.
    """

    admitted_objectives = ['deficit', 'target']

    def __init__(self, target_col, candidate_col, strata_cols, score_col,
                 imputation_target_srs,
                 objective='deficit',
                 imputable_col=None, weight_col=None, transfer_strategy=None,
                 verbose=False, copy=True, force=False, debug=False):

        self.target_col = target_col
        self.candidate_col = candidate_col
        self.strata_cols = strata_cols
        self.score_col = score_col
        self.imputation_target_srs = imputation_target_srs
        self.imputable_col = imputable_col
        self.weight_col = weight_col
        self.transfer_strategy = transfer_strategy
        self.verbose = verbose
        self.copy = copy
        self.force = force
        assert objective in self.admitted_objectives, ValueError(textwrap.fill(
            f'`objective` parameter must be  in {self.admitted_objectives}'
        ))
        self.objective = objective
        self.debug = debug
        self.debug_dict = defaultdict(lambda: {})

        # attribute to be fitted
        self.imputation_scheme = None

    def _assert_df_compatible_with_imputer(self, df):
        """
        Verifies if all column labels necessary to the imputation
        process are present on DataFrame `df`.
        """
        mandatory_columns = set(
            self.strata_cols + [
                self.imputable_col, self.score_col, self.target_col,
                self.candidate_col
            ] + self.imputation_target_srs.index.names)
        non_present_cols_on_df = pd.Index(mandatory_columns).difference(
            df.columns).difference(([None]))
        assert len(non_present_cols_on_df) == 0, \
            "The following columns are not present on `df`:\n" + \
            f"{non_present_cols_on_df}"
        return True

    def _infer_uncorrected_imputation_scheme(self, df_, debug=False):
        """
        Infers the number of observations which need to be imputed 
        across every strata, without correcting by `transfer_strategy`.
        """

        # calculate already present on df
        if self.weight_col is not None:
            df_['_satisfied'] = df_[
                [self.target_col, self.weight_col]].product(1)
        else:
            df_['_satisfied'] = df_[self.target_col]
        present_per_target_sum = df_.groupby(self.strata_cols)[
            '_satisfied'].sum()

        # infer missing strata distribution on `imputation_target_srs`
        # suposing proportions should be kept equal
        target_strata_cols = list(self.imputation_target_srs.index.names)
        satisfied_per_target_strata = present_per_target_sum.reset_index(
        ).groupby(target_strata_cols)['_satisfied'].sum()
        proportions_srs = present_per_target_sum / satisfied_per_target_strata

        # handle the case where no satified cases where present on `df`
        if satisfied_per_target_strata.eq(0).all():
            print(textwrap.fill(
                'There are no observations on target column. '
                '`imputation_target_srs` will be used as imputation'
                'scheme.'))
            if all([
                strat_col in target_strata_cols for strat_col in
                self.strata_cols
            ]):
                inferred_target_srs = self.imputation_target_srs
            else:
                raise NotImplementedError(textwrap.fill(
                    'As `imputation_target_srs` is used as imputation '
                    'scheme, its index names should coincide with '
                    '`strata_cols`.'
                ))
        else:
            if satisfied_per_target_strata.eq(0).any():
                warnings.warn(textwrap.fill(
                    "There are divisions by zero in `proportion_srs`"
                    "calculation"), RuntimeWarning, stacklevel=2)
            inferred_target_srs = proportions_srs * self.imputation_target_srs

        # get uncorrected imputation scheme (raw deficit)
        deficit_srs = inferred_target_srs.subtract(present_per_target_sum).fillna(0)
        if (deficit_srs < 0).any():
            raise NotImplementedError(
                "There are negative values on imputation scheme"
            )
        if self.debug:
            self.debug_dict['_infer_uncorrected_imputation_scheme'] = {
                'present_per_target_sum': present_per_target_sum,
                'proportions_srs': proportions_srs,
                'inferred_target_srs': inferred_target_srs,
                'deficit_srs': deficit_srs
            }

        # assign imputation scheme depeding on the objective of the
        # imputation
        self.imputation_scheme = deficit_srs if self.objective == 'deficit' \
            else inferred_target_srs

    def _infer_corrected_imputation_scheme(self, df):
        """
        If the imputation_scheme is not feasible, it corrects it
        according to `transfer_strategy`.
        """
        index_names = self.imputation_scheme.index.names

        # calculate imputable observations per strata
        imputable_df = df[df[self.imputable_col]].copy() if \
            self.imputable_col is not None else df
        imputable_df['weighted_impute'] = imputable_df[self.candidate_col] * (
            imputable_df['weight'] if self.weight_col is not None else 1)
        imputable_obs_per_strata_srs = imputable_df.groupby(
            index_names, sort=False)['weighted_impute'].sum()


        # check if imputation scheme is feasible
        if not self._check_compatible_imputation_scheme(
                imputable_obs_per_strata_srs):
            # correct imputation scheme
            print('entered_correction') if self.verbose else None
            self._correct_imputation_scheme(imputable_obs_per_strata_srs)

    def _check_compatible_imputation_scheme(
            self, imputable_obs_per_strata_srs,
            updated_imputation_scheme=None, tolerance=1e-2):
        """
        Checks is the number of imputable observations per strata is
        enough for every strata deficit.

        Parameters
        ----------
        imputable_obs_per_strata_srs : Series
            Indicates the available imputable observations per strata.
        updated_imputation_scheme : None or Series
            If None, `imputable_obs_per_strata_srs` is compared against
            `imputation_scheme`. If Series, `imputable_obs_per_strata_srs`
            is compared against it. Defaults to `None`.
        tolerance : float
            Used for avoiding numeric errors on the difference between
            `imputable_obs_per_strata_srs` and the imputation scheme.
            Defaults to `1e-2`.
        """
        updated_imputation_scheme = \
            self.imputation_scheme if updated_imputation_scheme is None else \
                updated_imputation_scheme
        return (updated_imputation_scheme - imputable_obs_per_strata_srs).lt(
            tolerance).all()

    def _correct_imputation_scheme(self, imputable_obs_per_strata_srs):
        """
        Modifies `imputation_scheme` to make the imputation feasible in
        case `transfer_strategy` is not None.

        Parameters
        ----------
        imputable_obs_per_strata_srs : Series
            Contais the total imputable amount on each strata.
        """
        # a copy of imputation scheme will modulate control flow
        updated_imputation_scheme = self.imputation_scheme.copy()

        # account for the number of transfer tried
        transfer_tried_dict = defaultdict(lambda: 0)

        for transfer_tuple in self.transfer_strategy:
            idx_level, transfer_map = transfer_tuple

            # transfer need to be done iteratively in case of no bijective
            # mappings
            for transfer_src, transfer_dst in transfer_map.items():
                # calculate the number of amounts needed to be transferred
                to_impute_minus_imputable_srs = \
                    updated_imputation_scheme.subtract(
                        imputable_obs_per_strata_srs)
                to_transfer_srs = to_impute_minus_imputable_srs[
                    to_impute_minus_imputable_srs > 0]

                # ensure transfer amounts can be allocated on dst strata
                # display(to_transfer_srs)
                try:
                    feasible_transfer_srs = np.minimum(
                        # rename index to match dst strata
                        to_transfer_srs.xs(
                            transfer_src, level=idx_level, drop_level=False).rename(
                            index={transfer_src: transfer_dst}, level=idx_level
                        ), - to_impute_minus_imputable_srs).dropna()
                except KeyError as ex:
                    if transfer_src not in \
                        self.imputation_scheme.index.get_level_values(
                            idx_level):
                        raise ex
                    else:
                        pass

                # transfer imputation amounts from saturated to unsaturated
                # strata
                updated_imputation_scheme = updated_imputation_scheme.add(
                    feasible_transfer_srs.reindex(
                        updated_imputation_scheme.index).fillna(0))
                updated_imputation_scheme = updated_imputation_scheme.subtract(
                    # rename index to match src strata
                    feasible_transfer_srs.rename(
                        index={transfer_dst: transfer_src}, level=idx_level
                    ).reindex(updated_imputation_scheme.index).fillna(0))

            transfer_tried_dict[idx_level] += 1

            # update imputation scheme
            if self.verbose:
                print('updated_imputation_scheme')
                display(dict(transfer_tried_dict))
            self.imputation_scheme = updated_imputation_scheme

            # once a `transfer_map` has been completely implemented check if
            # further `transfer map`'s need to be executed
            if self._check_compatible_imputation_scheme(
                    imputable_obs_per_strata_srs,
            ):
                break

        # in case no feasible imputation scheme was found
        else:
            deficit_srs = updated_imputation_scheme.subtract(
                imputable_obs_per_strata_srs)
            if self.debug:
                self.debug_dict['_correct_imputation_scheme'] = {
                    'updated_imputation_scheme': updated_imputation_scheme,
                    'imputable_obs_per_strata_srs': imputable_obs_per_strata_srs,
                    'deficit_srs': deficit_srs,
                }
            positive_deficit_str = textwrap.fill(
                    '`transfer_strategy` parameter is not able to correct the '
                    'imputation scheme for attaining the imputation target. '
                    'The following number of observations are required to '
                    'attain imputation scheme:'
                ) + f'\n{deficit_srs[deficit_srs > 0]}'
            if not self.force:
                raise ValueError(positive_deficit_str)
            else:
                print(
                    positive_deficit_str,
                    'As `force` is True, imputation does not raise error',
                    sep='\n'
                )

    def _get_imputation_srs(self, df, tolerance=1e-2):
        """
        Returns a Series containing the values and index of observations
        from `target_col` to be imputed on `df`.
        Parameters
        ----------
        tolerance : float
            Used for avoiding numeric errors on the difference between
            `imputable_obs_per_strata_srs` and the imputation scheme.
            Defaults to `1e-2`.
        """
        index_names = self.imputation_scheme.index.names

        # get cumsum of imputable observations, ordered by score
        imputable_df = df[df[self.imputable_col]].copy() if \
            self.imputable_col is not None else df
        imputable_df = imputable_df.sort_values(
            index_names.union([self.score_col]), ascending=False)
        imputable_df['weighted_impute'] = imputable_df[self.candidate_col] * (
            imputable_df['weight'] if self.weight_col is not None else 1)
        imputable_df['impute_cumsum'] = imputable_df.groupby(
            index_names, as_index=False, sort=False)[
            'weighted_impute'].transform('cumsum')

        # join number of observations per strata
        imputable_df = imputable_df.merge(
            self.imputation_scheme.to_frame(name='n_obs_to_impute').reset_index(
                ), on=self.strata_cols, how='left').set_index(
            imputable_df.index)

        # calculate cummulated difference on each strata
        imputable_df['balance'] = imputable_df.n_obs_to_impute - imputable_df.impute_cumsum

        # check if stratification is compatible with imputation targets
        last_balance_srs = imputable_df.groupby(self.strata_cols, sort=False)[
            'balance'].last()
        if (last_balance_srs > tolerance).any():
            positive_balances_str = textwrap.fill(
                'There are strata where the number of imputable observations '
                'is not enough for attaining the imputation scheme target. '
                'Check if `transfer_strategy` could be used for transferring '
                'imputable amounts between strata') + \
                f'\n{last_balance_srs[last_balance_srs > 0]}'
            if self.debug:
                self.debug_dict['_get_imputation_srs'] = {
                    'last_balance_srs': last_balance_srs
                }
            if not self.force:
                raise ValueError(positive_balances_str)
            else:
                print(
                    positive_balances_str,
                    'As `force` is True, imputation does not raise error',
                    sep='\n'
                )

        # get balance closest to zero per strata
        imputable_df['balance_closest_to_zero'] = imputable_df.groupby(
            index_names, sort=False, as_index=False)['balance'].transform(
            lambda srs: srs.iat[srs.abs().argmin()])

        # select imputed observations
        imputable_df['imputed'] = imputable_df['balance'] >= imputable_df['balance_closest_to_zero']

        # get index of imputed observations
        return imputable_df.loc[imputable_df.imputed, self.candidate_col]

    def fit(self, df, y=None):
        """Fit consist in inferring the imputation scheme"""

        if self.imputation_scheme is None:

            # get imputation scheme
            self._infer_uncorrected_imputation_scheme(df)

            # check for unfeasible allocations if `transfer_strategy` is
            # defined
            if self.transfer_strategy is not None:
                self._infer_corrected_imputation_scheme(df)

        return self


    def transform(self, df):
        """
        Joins a column to `df` with the imputed version of `target_col`.
        It calls all other methods defined on the class.
        """
        # work in copy
        df_ = df.copy() if self.copy else df

        assert self.imputation_scheme  is not None, "`transform` need " + \
        "always to be called after `fit` method"
        assert self._assert_df_compatible_with_imputer(df_)

        # get impute series
        imputation_srs = self._get_imputation_srs(df)

        # get imputed column
        df_.loc[imputation_srs.index, '_imputed'] = imputation_srs
        df_.loc[:, '_imputed'] = df_['_imputed'].fillna(0)

        # get imputed target column
        df_.loc[:, f'imputed_{self.target_col}'] = df_[self.target_col] + df_[
            '_imputed']

        return df_

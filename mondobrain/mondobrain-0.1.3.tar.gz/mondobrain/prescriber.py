from io import BytesIO
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

import mondobrain as mb
from mondobrain.core.frame import MondoDataFrame
from mondobrain.core.meta import BaseExploration
from mondobrain.core.series import MondoSeries
from mondobrain.dd_transformer import DDTransformer
from mondobrain.error import NotEnoughPointsError
from mondobrain.utils import meta as meta_utils, utilities


class Solver:
    """
    MondoBrain Solver object.

    Applies a stochastic search for the global maximum Z-score with respect to
    a defined dependent variable and target class, in cases of "discrete" variables
    or target min/max mean in the cases of "continuous" variables.

    Parameters
    ----------
    min_size_frac: float (optional), default=0.2
        Value between 0.0 and 1.0 that defines the minimum number of points needed
        for a valid rule discovered by the MondoBrain solver.

    min_purity: float (optional), default=0.0
        Value between 0.0 and 1.0 that defines the minimum purity needed for a valid
        rule discovered by the MondoBrain solver.

        Purity here is defined as the mean of the target variable distribution.

    max_cycles: int (optional), default=90
        Value greater than 0 that defines the total cycles the MondoBrain solver should
        commit in order to find a valid rule.

    Examples
    --------
    Using the solver to find a rule

    >>> mb.api_key = "<API KEY>"
    >>> mb.api_secret = "<API SECRET>"
    >>> solver = mb.Solver()
    >>> solver.fit(mdf_explorable, mdf_outcome)
    >>> solver.rule
    {
        'sex': {'low': 'male', 'high': 'male'},
        'class': {'low': 2, 'high': 3},
        'parch': {'low': 0, 'high': 0},
        'ticketnumber': {'low': 2152.0, 'high': 3101281.0}
    }
    >>> solver.score
    12.974682681486312


    """

    def __init__(
        self, min_size_frac=0.2, min_purity=0.0, max_cycles=90,
    ):
        self.min_size_frac = min_size_frac
        self.min_purity = min_purity
        self.max_cycles = max_cycles

    @staticmethod
    def _is_one_dim_solve(explorable_vars):
        return explorable_vars.shape[1] == 1

    @staticmethod
    def _get_timeout(n_points, n_features, lg_coefficient=3.5, max_cycles=90):

        lg_timeout = int(lg_coefficient * np.sqrt(n_points * n_features / 2))
        min_timeout = np.minimum(lg_timeout, max_cycles)

        return int(np.maximum(1, min_timeout))

    @staticmethod
    def _get_dataset_buffer(df: pd.DataFrame):
        buffer = BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)
        return buffer

    def _run_solve(self, mdf: MondoDataFrame, outcome: str, target: str):
        encoder = DDTransformer(mdf)
        edf = utilities.encode_dataframe(mdf, encoder)
        target_encoded = utilities.encode_value(mdf, outcome, target, encoder)
        outcome_encoded = encoder.original_to_encoded_column(outcome)

        edf, _ = utilities.sample_if_needed(edf, target_encoded, outcome_encoded)

        enough_points = utilities.has_enough_values(
            edf, target_encoded, outcome_encoded
        )
        if not enough_points:
            raise NotEnoughPointsError(
                "Cannot run solver unless there are at least {0} points.".format(
                    utilities.MIN_SOLVER_SIZE
                )
            )

        # Solve Behavior isn't supported by file endpoint yet
        timeout = self._get_timeout(
            edf.shape[0], edf.shape[1] - 1, max_cycles=self.max_cycles
        )

        buf = Solver._get_dataset_buffer(edf)
        task = mb.api.solve_start_file(
            outcome=outcome_encoded,
            target=target_encoded,
            data=buf,
            timeout=timeout,
            min_size_frac=self.min_size_frac,
        )
        result = mb.api.solve_result(id=task["id"])

        rule_encoded = result["rule"]
        rule_decoded = utilities.decode_rule(rule_encoded, encoder)

        # Stats
        if mdf[outcome].var_type == "discrete":
            # Discrete Stats - operate in original space
            mdf_applied = utilities.apply_rule_to_df(mdf, rule_decoded)

            sample_stats = utilities.get_stats(mdf_applied, outcome, target)
            score = utilities.score_rule(mdf, rule_decoded, outcome, target)
        else:
            # Continous Stats - operate in encoded space
            edf_applied = utilities.apply_rule_to_df(edf, rule_encoded)

            sample_stats = utilities.get_stats(
                edf_applied, outcome_encoded, target_encoded
            )
            score = utilities.score_rule(
                edf, rule_encoded, outcome_encoded, target_encoded
            )

        return rule_decoded, sample_stats, score

    @property
    def max_cycles(self):
        return self._max_cycles

    @max_cycles.setter
    def max_cycles(self, value):
        if value > 0:
            self._max_cycles = value
        else:
            raise ValueError("'max_cycles' must be greater than 0.")

    def get_rule_data(self, dataset=None, xrule=False):
        """
        Return a MondoDataFrame that is filtered or not filtered by a rule

        Parameters
        ----------
        dataset: MondoDataFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number of
            features.

        xrule: Bool, optional (default=False)
            Where `xrule` refers to `not rule` and, if True, returns the portion of the
            dataset not defined by the rule and False returns the portion of the dataset
            defined by the rule.

        """

        if xrule:
            idx = utilities.apply_rule_to_df(dataset, self.rule).index
            xidx = dataset.index[~np.in1d(dataset.index, idx)]
            return dataset.loc[xidx]
        else:
            return utilities.apply_rule_to_df(dataset, self.rule)

    def fit(self, m_X, m_y, cv=None):
        """
        Fit the Solver with the provided data.

        Parameters
        ----------
        m_X: MondoDataFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number
            of features

        m_y: MondoSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X

        cv: int or sklearn.model_selection object, optional (default=None)
            The number of folds (n_splits) used in cross validation, or a Sci-Kit
            Learn model splitter, such as StratifiedKFold, ShuffleSplit, etc.  If a
            number is given, the KFold technique is used.  If the value is None,
            the rule does not get cross-validated.

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        if isinstance(cv, int) or isinstance(cv, float):
            cv = KFold(n_splits=cv, shuffle=True)

        if cv is None:
            X_train, X_test, y_train, y_test = m_X, None, m_y, None
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                m_X, m_y, test_size=0.33, random_state=1337
            )
            y_train.target_class = y_test.target_class = m_y.target_class

        mdf = MondoDataFrame(pd.concat((MondoDataFrame(y_train), X_train), axis=1))

        outcome = m_y.name
        target = m_y.target_class

        self.rule, sample_stats, self.score = self._run_solve(mdf, outcome, target)

        self.size = sample_stats["size"]
        self.mean = sample_stats["mean"]
        self.rule_data = self.get_rule_data(mdf)

        if cv is not None:
            self.validation = utilities.cross_validate_rule(
                self.rule, X_test, y_test, cv=cv, score=self.score
            )

    def fit_predicted(
        self, m_X, m_y, m_y_predicted, predicted=False, max_depth=None, min_score=0,
    ):
        """
        Fit the Solver with the provided data but optimizing on the error between
        ground truth and the return values of any statistical model.

        Parameters
        ----------

        m_X: MondoDataFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number of
            features.

        m_y: MondoSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X.

        m_y_predicted: MondoSeries, Series, or array (n_samples,), default=None
            Where n_samples is the number of samples and aligns with n_samples of m_y.
            * If provided, `m_y_predicted` will be compare against `m_y` to find a rule
            that explains differences between "correct" and "incorrect" predictions.

        predicted: Bool, optional (default=False)
            Defines the focus of the exploration. To find rules where the provided
            `m_y_predicted` is predicted or where it is not predicted.

        max_depth: Int, optional (default=None)
            Sets a maximum number of levels in to split rules and incidentally the
            subsamples defined by the rules.
            Default `None` allows maximum number of splits.

        min_score: Int, optional (default=0)
            Sets a minimum Z-score found by rules as a threshold for rejecting rules.
            If a rule is rejected, exploration down that branch will bet terminated.

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        if m_y.var_type == "discrete":
            cond = m_y_predicted == m_y
            y_error = MondoSeries(
                np.where(cond, "correct", "incorrect"),
                name="prediction",
                index=m_y.index,
            )
            y_error.target_class = "correct" if predicted else "incorrect"
        else:
            y_error = MondoSeries(
                np.abs(m_y_predicted - m_y), name="residual", index=m_y.index
            )
            y_error.target_class = "min" if predicted else "max"

        mdf = MondoDataFrame(pd.concat((MondoDataFrame(y_error), m_X), axis=1))

        outcome = y_error.name
        target = y_error.target_class

        self.rule_tree = dict()

        def evaluate(data, depth=0, current="IN", prior=(0, "IN")):
            if all(
                (
                    data.shape[0] > 1,
                    data[outcome].unique().shape[0] > 1,
                    depth <= max_depth if max_depth is not None else depth <= 1e6,
                )
            ):
                self.rule, sample_stats, self.score = self._run_solve(
                    data, outcome, target
                )
                self.size = sample_stats["size"]
                self.mean = sample_stats["mean"]

                if self.score > min_score:
                    key = prior + (depth, current)
                    self.rule_tree[key] = {
                        "rule": self.rule,
                        "score": self.score,
                        "size": self.size,
                        "mean": self.mean,
                    }

                    rule_data = self.get_rule_data(data).copy()
                    xrule_data = self.get_rule_data(data, xrule=True).copy()

                    try:
                        evaluate(rule_data, depth + 1, "IN", key)
                    except NotEnoughPointsError:
                        pass
                    try:
                        if (key + (depth + 1, "IN")) in self.rule_tree:
                            evaluate(xrule_data, depth + 1, "OUT", key)
                    except NotEnoughPointsError:
                        pass

        evaluate(mdf)

    def fit_meta(self, m_X, m_y, exp: BaseExploration):
        """
        Discover feature rules with the provided data.

        Parameters
        ----------
        m_X: MondoDataFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the number
            of features

        m_y: MondoSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with n_samples of m_X

        exp: an object that extends core.meta.BaseExploration
            The type of exploration used to discover feature rules

        """

        explorable_vars = [col for col in m_X.columns if col != m_y.name]
        m_X = m_X[explorable_vars].copy()

        mdf = MondoDataFrame(pd.concat((MondoDataFrame(m_y), m_X), axis=1))
        outcome = m_y.name

        encoder = DDTransformer(mdf)
        edf = utilities.encode_dataframe(mdf, encoder)
        outcome_encoded = encoder.original_to_encoded_column(outcome)
        exp.encode_options(mdf, outcome, encoder)

        edf, _ = utilities.sample_if_needed(edf, None, outcome_encoded)

        data = json.loads(edf.to_json(orient="records"))
        timeout = self._get_timeout(
            edf.shape[0], edf.shape[1] - 1, max_cycles=self.max_cycles
        )
        options = {
            "outcome": outcome_encoded,
            "data": data,
            "min_size_frac": self.min_size_frac,
            "timeout": timeout,
        }

        exp.explore(options)

        exp.decode_results(edf, outcome_encoded, encoder)

        rules = exp.result["rules"]
        meta_mdf = meta_utils.apply_meta_rules_to_df(rules, mdf)

        self.meta = {"rules": rules, "df": meta_mdf}

    def cross_validate(self, m_X, m_y, cv=3):
        """
        Cross validate rules against the provided data using a leave-one-out
            cross validation technique.

        Parameters
        ----------

        m_X: MondoDataFrame of shape (n_samples, n_features)
            Where n_samples is the number of samples and n_features is the
            number of features.

        m_y: MondoSeries of shape (n_samples,)
            Where n_samples is the number of samples and aligns with
            n_samples of m_X.

        cv: int or sklearn.model_selection object, optional (default=3)
            The number of folds (n_splits) used in cross validation, or a Sci-Kit
            Learn model splitter, such as StratifiedKFold, ShuffleSplit, etc.  If a
            number is given, the KFold technique is used.

        Returns
        -------

        scores: dict of float arrays of shape (n_splits,).  The possible keys for
            this dictionary are as follows:
            - train_scores: an array of scores when finding rules on validation sets
            - train_sizes: an array of sizes of rules on the training sets
            - test_scores: an array of scores when applying the rule on the test set
            - test_sizes: an array of sizes of rules on the test sets
            - rules: an array of rules (see solver.rule for object definition)
            - avg_loss: the mean squared error between train and test scores

        """

        if isinstance(cv, int) or isinstance(cv, float):
            cv = KFold(n_splits=cv, shuffle=True)

        X_train, X_test, y_train, y_test = train_test_split(
            m_X, m_y, test_size=0.33, random_state=1337
        )
        y_train.target_class = y_test.target_class = m_y.target_class

        mdf = MondoDataFrame(pd.concat((MondoDataFrame(y_test), X_test), axis=1))

        # For use in scoring later (_run_solve handles in-flight encoding)
        encoder = DDTransformer(mdf)
        edf = utilities.encode_dataframe(mdf, encoder)

        train_scores, train_sizes = [], []
        test_scores, test_sizes = [], []
        rules = []

        for train_index, test_index in cv.split(X_train, y_train):
            X_train_curr = X_train.iloc[train_index]
            y_train_curr = y_train.iloc[train_index]

            mdf_cur = MondoDataFrame(
                pd.concat((MondoDataFrame(y_train_curr), X_train_curr), axis=1)
            )

            outcome = m_y.name
            target = m_y.target_class

            train_rule, train_sample_stats, train_score = self._run_solve(
                mdf_cur, outcome, target
            )
            train_size = train_sample_stats["size"]

            if m_y.var_type == "discrete":
                # Discrete Stats - operate in original space
                mdf_applied = utilities.apply_rule_to_df(mdf, train_rule)

                test_sample_stats = utilities.get_stats(mdf_applied, outcome, target)
                test_score = utilities.score_rule(mdf, train_rule, outcome, target)
                test_size = test_sample_stats["size"]
            else:
                # Continous Stats - operate in encoded space
                test_rule = utilities.encode_rule(train_rule, encoder)
                outcome_encoded = encoder._column_encoder[outcome]

                edf_applied = utilities.apply_rule_to_df(edf, test_rule)

                test_sample_stats = utilities.get_stats(
                    edf_applied, outcome_encoded, target
                )
                test_score = utilities.score_rule(
                    edf, test_rule, outcome_encoded, target
                )
                test_size = test_sample_stats["size"]

            train_scores.append(train_score)
            train_sizes.append(train_size)
            test_scores.append(test_score)
            test_sizes.append(test_size)
            rules.append(train_rule)

        mse = np.mean((np.array(train_scores) - np.array(test_scores)) ** 2)

        result = {
            "train_scores": train_scores,
            "train_sizes": train_sizes,
            "test_scores": test_scores,
            "test_sizes": test_sizes,
            "rules": rules,
            "avg_loss": mse,
        }

        return result

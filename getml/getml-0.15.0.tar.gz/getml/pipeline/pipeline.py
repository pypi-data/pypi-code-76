# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
This submodule contains the Pipeline, which is the main
class for feature learning and prediction.
"""

import copy
import json
import numbers
import socket
import time
from datetime import datetime

import numpy as np

import getml.communication as comm
import getml.pipeline.scores as metrics
from getml import data
from getml.data import Placeholder, _decode_placeholder
from getml.data.helpers import (
    _is_subclass_list,
    _is_typed_list,
    _remove_trailing_underscores,
)
from getml.data.visualization import _make_link, _monitor_url
from getml.feature_learning import _FeatureLearner
from getml.feature_learning.loss_functions import _classification_loss
from getml.helpers import _html, _str
from getml.predictors import _classification_types, _Predictor
from getml.preprocessors.preprocessor import _Preprocessor

from .columns import Columns
from .features import Features
from .helpers import (
    _check_df_types,
    _make_id,
    _parse_fe,
    _parse_pred,
    _parse_preprocessor,
    _print_time_taken,
    _replace_with_nan_maybe,
    _transform_peripheral,
    _unlist_maybe,
)
from .metrics import Metrics
from .score import ClassificationScore, RegressionScore
from .scores import (
    _all_scores,
    _classification_scores,
    accuracy,
    auc,
    cross_entropy,
    mae,
    rmse,
    rsquared,
)
from .scores_container import Scores

# --------------------------------------------------------------------

NOT_FITTED = "NOT FITTED"


class Pipeline:
    """
    A Pipeline is the main class for feature learning and prediction.

    Args:
        population (:class:`getml.data.Placeholder`, optional):
            Abstract representation of the population table,
            which defines the statistical population and contains
            the target variables.

        peripheral (Union[:class:`~getml.data.Placeholder`, List[:class:`~getml.data.Placeholder`]], optional):
            Abstract representations of the additional tables used to
            augment the information provided in `population`. These
            have to be the same objects that got
            :meth:`~getml.data.Placeholder.join` on the
            `population` :class:`~getml.data.Placeholder` and
            their order strictly determines the order of the
            peripheral :class:`~getml.data.DataFrame` provided in
            the 'peripheral_tables' argument of
            :meth:`~getml.pipeline.Pipeline.check`,
            :meth:`~getml.pipeline.Pipeline.fit`,
            :meth:`~getml.pipeline.Pipeline.predict`,
            :meth:`~getml.pipeline.Pipeline.score`, and
            :meth:`~getml.pipeline.Pipeline.transform`.

        feature_learners (Union[:class:`~getml.feature_learning._FeatureLearner`, List[:class:`~getml.feature_learning._FeatureLearner`]], optional):
            The feature learner(s) to be used.
            Must be from :mod:`~getml.feature_learning`.
            A single feature learner does not have to be wrapped
            in a list.

        feature_selectors (Union[:class:`~getml.predictors._Predictor`, List[:class:`~getml.predictors._Predictor`]], optional):
            Predictor(s) used to select the best features.
            Must be from :mod:`~getml.predictors`.
            A single feature selector does not have to be wrapped
            in a list.
            Make sure to also set *share_selected_features*.

        predictors (Union[:class:`~getml.predictors._Predictor`, List[:class:`~getml.predictors._Predictor`]], optional):
            Predictor(s) used to generate the predictions.
            If more than one predictor is passed, the predictions
            generated will be averaged.
            Must be from :mod:`~getml.predictors`.
            A single predictor does not have to be wrapped
            in a list.

        tags (List[str], optional): Tags exist to help you organize your pipelines.
            You can add any tags that help you remember what you were
            trying to do.

        include_categorical (bool, optional): Whether you want to pass categorical columns
            in the population table to the predictor.

        share_selected_features(float, optional): The share of features you want the feature
            selection to keep. When set to 0.0, then all features will be kept.

    Example:

        We assume that you have already set up your
        data model using :class:`~getml.data.Placeholder`,
        your feature learners (refer to :mod:`~getml.feature_learning`)
        as well as your feature selectors and predictors
        (refer to :mod:`~getml.predictors`, which can be used
        for prediction and feature selection).

        .. code-block:: python

            pipe = getml.pipeline.Pipeline(
                tags=["multirel", "relboost", "31 features"],
                population=population_placeholder,
                peripheral=[order_placeholder, trans_placeholder],
                feature_learners=[feature_learner_1, feature_learner_2],
                feature_selectors=feature_selector,
                predictors=predictor,
                share_selected_features=0.5
            )

            # "order" and "trans" refer to the names of the
            # placeholders.
            pipe.check(
                population_table=population_training,
                peripheral_tables={"order": order, "trans": trans}
            )

            pipe.fit(
                population_table=population_training,
                peripheral_tables={"order": order, "trans": trans}
            )

            pipe.score(
                population_table=population_testing,
                peripheral_tables={"order": order, "trans": trans}
            )
    """

    # ------------------------------------------------------------

    def __init__(
        self,
        population=None,
        peripheral=None,
        preprocessors=None,
        feature_learners=None,
        feature_selectors=None,
        predictors=None,
        tags=None,
        include_categorical=False,
        share_selected_features=0.5,
    ):

        # ------------------------------------------------------------

        population = population or Placeholder("POPULATION")

        peripheral = peripheral or []

        preprocessors = preprocessors or []

        feature_learners = feature_learners or []

        feature_selectors = feature_selectors or []

        predictors = predictors or []

        tags = tags or []

        # ------------------------------------------------------------

        if not isinstance(preprocessors, list):
            preprocessors = [preprocessors]

        if not isinstance(feature_learners, list):
            feature_learners = [feature_learners]

        if not isinstance(feature_selectors, list):
            feature_selectors = [feature_selectors]

        if not isinstance(predictors, list):
            predictors = [predictors]

        if not isinstance(peripheral, list):
            peripheral = [peripheral]

        if not isinstance(tags, list):
            tags = [tags]

        # ------------------------------------------------------------

        self._id = NOT_FITTED

        self.type = "Pipeline"

        # ------------------------------------------------------------

        self.preprocessors = preprocessors
        self.feature_learners = feature_learners
        self.feature_selectors = feature_selectors
        self.include_categorical = include_categorical
        self.peripheral = peripheral
        self.population = population
        self.predictors = predictors
        self.tags = Tags(tags) or Tags([])
        self.share_selected_features = share_selected_features

        # ------------------------------------------------------------

        self._scores = None

        self._targets = None

        # ------------------------------------------------------------

        Pipeline._supported_params = list(self.__dict__.keys())

        # ------------------------------------------------------------

        self.validate()

    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance of the
        :class:`~getml.pipeline.Pipeline` with another one.

        Args:
            other: Another :class:`~getml.pipeline.Pipeline` to
                compare the current instance against.

        Returns:
            bool: Whether the current instance and `other` share the
                same content.

        Raises:
            TypeError: If `other` is not of class
                :class:`~getml.pipeline.Pipeline`
        """

        if not isinstance(other, Pipeline):
            raise TypeError("A Pipeline can only be compared to another Pipeline")

            # ------------------------------------------------------------

        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False

            # ------------------------------------------------------------

        for kkey in self.__dict__:

            if kkey not in other.__dict__:
                return False

            # Take special care when comparing numbers.
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False

            elif self.__dict__[kkey] != other.__dict__[kkey]:
                return False

            # ------------------------------------------------------------

        return True

    # ----------------------------------------------------------------

    def __repr__(self):
        obj_dict = self._make_object_dict()

        repr_str = _str(obj_dict)

        if self.fitted:
            repr_str += "\n\nurl: " + self._make_url()

        return repr_str

    # ----------------------------------------------------------------

    def _repr_html_(self):
        obj_dict = self._make_object_dict()

        html = _html(obj_dict)

        if self.fitted:
            url_str = "url: " + self._make_url()
            url_str = _make_link(url_str)
            html += "<br><pre>" + url_str + "</pre>"

        return html

    # ------------------------------------------------------------

    def _check_classification_or_regression(self):
        """
        Checks whether there are inconsistencies in the algorithms used
        (mixing classification and regression algorithms).
        """

        # -----------------------------------------------------------

        all_classifiers = all(
            [
                elem.loss_function in _classification_loss
                for elem in self.feature_learners
            ]
        )

        all_classifiers = all_classifiers and all(
            [elem.type in _classification_types for elem in self.feature_selectors]
        )

        all_classifiers = all_classifiers and all(
            [elem.type in _classification_types for elem in self.predictors]
        )

        # -----------------------------------------------------------

        all_regressors = all(
            [
                elem.loss_function not in _classification_loss
                for elem in self.feature_learners
            ]
        )

        all_regressors = all_regressors and all(
            [elem.type not in _classification_types for elem in self.feature_selectors]
        )

        all_regressors = all_regressors and all(
            [elem.type not in _classification_types for elem in self.predictors]
        )

        # -----------------------------------------------------------

        if not all_classifiers and not all_regressors:
            raise ValueError(
                """You are mixing classification and regression
                                algorithms. Please make sure that your feature learning
                                algorithms consistently have classification loss functions
                                (like CrossEntropyLoss) or consistently have regression
                                loss functions (like SquareLoss). Also make sure that your
                                feature selectors and predictors are consistently classifiers
                                (like XGBoostClassifier or LogisticRegression) or consistently
                                regressors (like XGBoostRegressor or LinearRegression).
                             """
            )

        # -----------------------------------------------------------

        return all_classifiers

    # ------------------------------------------------------------

    def _check_whether_fitted(self):
        if not self.fitted:
            raise ValueError("Pipeline has not been fitted!")

    # ------------------------------------------------------------

    def _close(self, sock):
        """
        Raises:
            TypeError: If `sock` is not of type
                :py:class:`socket.socket`
        """

        if not isinstance(sock, socket.socket):
            raise TypeError("'sock' must be a socket.")

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".close"
        cmd["name_"] = self.id

        comm.send_string(sock, json.dumps(cmd))

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

    # ------------------------------------------------------------

    def _get_latest_score(self, score):
        nan_ = [np.nan] * len(self.targets)

        if score not in _all_scores:
            raise AttributeError(f"Not a valid score name: {score}")

        if not self.scored:
            return nan_

        if self.is_classification and score not in _classification_scores:
            return nan_

        if self.is_regression and score in _classification_scores:
            return nan_

        return self._scores[score]

    # ------------------------------------------------------------

    def _getml_deserialize(self):
        """
        Expresses the pipeline in a form the engine can understand.
        """

        cmd = dict()

        self_dict = self.__dict__

        cmd["name_"] = self.id

        for key, value in self_dict.items():
            cmd[key + "_"] = value

        del cmd["_id_"]
        del cmd["_scores_"]
        del cmd["_targets_"]

        return cmd

    # ----------------------------------------------------------------

    def _make_object_dict(self):
        obj_dict = copy.deepcopy(self.__dict__)

        obj_dict["population"] = self.population.name

        obj_dict["peripheral"] = [elem.name for elem in self.peripheral]

        obj_dict["preprocessors"] = [elem.type for elem in self.preprocessors]

        obj_dict["feature_learners"] = [elem.type for elem in self.feature_learners]

        obj_dict["feature_selectors"] = [elem.type for elem in self.feature_selectors]

        obj_dict["predictors"] = [elem.type for elem in self.predictors]

        return obj_dict

    # ----------------------------------------------------------------

    def _make_score_history(self):

        # ------------------------------------------------------------

        scores = self._scores["history"]
        scores = [_replace_with_nan_maybe(score) for score in scores]

        # ------------------------------------------------------------

        if self.is_classification:
            return [
                ClassificationScore(
                    date_time=datetime.strptime(
                        score.get("date_time"), "%Y-%m-%d %H:%M:%S"
                    ),
                    set_used=score.get("set_used"),
                    target=target,
                    accuracy=score.get(metrics.accuracy)[target_num],
                    auc=score.get(metrics.auc)[target_num],
                    cross_entropy=score.get(metrics.cross_entropy)[target_num],
                )
                for score in scores
                for target_num, target in enumerate(self.targets)
            ]

        # ------------------------------------------------------------

        return [
            RegressionScore(
                date_time=datetime.strptime(
                    score.get("date_time"), "%Y-%m-%d %H:%M:%S"
                ),
                set_used=score.get("set_used"),
                target=target,
                mae=score.get(metrics.mae)[target_num],
                rmse=score.get(metrics.rmse)[target_num],
                rsquared=score.get(metrics.rsquared)[target_num],
            )
            for score in scores
            for target_num, target in enumerate(self.targets)
        ]

    # ----------------------------------------------------------------

    def _make_url(self):
        url = _monitor_url()
        url += "getpipeline/" + comm._get_project_name() + "/" + self.id + "/0/"
        return url

    # ----------------------------------------------------------------

    def _parse_cmd(self, json_obj):

        ptype = json_obj["type_"]

        del json_obj["type_"]

        if ptype != "Pipeline":
            raise ValueError("Expected type 'Pipeline', got '" + ptype + "'.")

        # ------------------------------------------------------------

        preprocessors = [
            _parse_preprocessor(elem) for elem in json_obj["preprocessors_"]
        ]

        del json_obj["preprocessors_"]

        # ------------------------------------------------------------

        feature_learners = [_parse_fe(elem) for elem in json_obj["feature_learners_"]]

        del json_obj["feature_learners_"]

        # ------------------------------------------------------------

        feature_selectors = [
            _parse_pred(elem) for elem in json_obj["feature_selectors_"]
        ]

        del json_obj["feature_selectors_"]

        # ------------------------------------------------------------

        predictors = [_parse_pred(elem) for elem in json_obj["predictors_"]]

        del json_obj["predictors_"]

        # ------------------------------------------------------------

        population = _decode_placeholder(json_obj["population_"])

        del json_obj["population_"]

        # ------------------------------------------------------------

        peripheral = [_decode_placeholder(elem) for elem in json_obj["peripheral_"]]

        del json_obj["peripheral_"]

        # ------------------------------------------------------------

        id_ = json_obj["name_"]

        del json_obj["name_"]

        # ------------------------------------------------------------

        kwargs = _remove_trailing_underscores(json_obj)

        self.__init__(
            population=population,
            peripheral=peripheral,
            preprocessors=preprocessors,
            feature_learners=feature_learners,
            feature_selectors=feature_selectors,
            predictors=predictors,
            **kwargs,
        )

        self._id = id_

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    def _parse_json_obj(self, all_json_objs):

        # ------------------------------------------------------------

        obj = all_json_objs["obj"]

        scores = all_json_objs["scores"]

        targets = all_json_objs["targets"]

        # ------------------------------------------------------------

        self._parse_cmd(obj)

        # ------------------------------------------------------------

        scores = _remove_trailing_underscores(scores)
        scores = _replace_with_nan_maybe(scores)

        self._scores = scores

        self._targets = targets

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    def _save(self):
        """
        Saves the pipeline as a JSON file.
        """

        # ------------------------------------------------------------
        # Send JSON command to getML engine

        cmd = dict()
        cmd["type_"] = self.type + ".save"
        cmd["name_"] = self.id

        comm.send(cmd)

    # ------------------------------------------------------------

    def _send(self):
        """Send the pipeline to the getML engine."""

        # -------------------------------------------

        if not isinstance(self.population, Placeholder):
            raise TypeError("'population' must be a valid data.Placeholder!")

        if not _is_typed_list(self.peripheral, Placeholder):
            raise TypeError(
                "'peripheral' must be an empty list or a list of getml.data.Placeholder"
            )

        # ------------------------------------------------------------

        self.validate()

        # ------------------------------------------------------------

        self._id = _make_id()

        cmd = self._getml_deserialize()

        comm.send(cmd)

        # ------------------------------------------------------------

        return self

    # ------------------------------------------------------------

    def _transform(
        self,
        peripheral_data_frames,
        population_data_frame,
        sock,
        score=False,
        predict=False,
        df_name="",
        table_name="",
    ):
        """Returns the features learned by the pipeline or writes them into a data base.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Population table. Targets will be ignored.
            peripheral_tables (List[:class:`getml.data.DataFrame`]):
                Peripheral tables.
                The peripheral tables have to be passed in the exact same order as their
                corresponding placeholders!
            sock (:py:class:`socket.socket`): TCP socket used to
                communicate with the getML engine.
            score (bool, optional): Whether the engine should calculate the
                scores of the pipeline based on the input data.
            predict (bool, optional): Whether the engine should transform the
                input data into features.
            df_name (str, optional):
                If not an empty string, the resulting features will be
                written into a newly created DataFrame, instead of returning
                them.
            table_name (str, optional):
                If not an empty string, the resulting features will be
                written into the data base, instead of returning
                them. See :ref:`unified_import_interface` for
                further information.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        """

        # ------------------------------------------------------------

        if isinstance(peripheral_data_frames, data.DataFrame):
            peripheral_data_frames = [peripheral_data_frames]

        # ------------------------------------------------------------

        if not _is_typed_list(peripheral_data_frames, data.DataFrame):
            raise TypeError(
                "'peripheral_data_frames' must be a getml.data.DataFrame or a list of those."
            )

        if not isinstance(population_data_frame, data.DataFrame):
            raise TypeError("'population_data_frame' must be a getml.data.DataFrame")

        if not isinstance(sock, socket.socket):
            raise TypeError("'sock' must be a socket.")

        if not isinstance(score, bool):
            raise TypeError("'score' must be of type bool")

        if not isinstance(predict, bool):
            raise TypeError("'predict' must be of type bool")

        if not isinstance(table_name, str):
            raise TypeError("'table_name' must be of type str")

        if not isinstance(df_name, str):
            raise TypeError("'df_name' must be of type str")

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id

        cmd["score_"] = score
        cmd["predict_"] = predict

        cmd["peripheral_names_"] = [df.name for df in peripheral_data_frames]
        cmd["population_name_"] = population_data_frame.name

        cmd["df_name_"] = df_name
        cmd["table_name_"] = table_name

        comm.send_string(sock, json.dumps(cmd))

        # ------------------------------------------------------------
        # Do the actual transformation

        msg = comm.log(sock)

        if msg == "Success!":
            if table_name == "" and df_name == "" and not score:
                yhat = comm.recv_matrix(sock)
            else:
                yhat = None
        else:
            comm.engine_exception_handler(msg)

        print()

        # ------------------------------------------------------------

        return yhat

    # ----------------------------------------------------------------

    @property
    def accuracy(self):
        """
        A convenience wrapper to rertrieve the accuracy of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.accuracy

    # ----------------------------------------------------------------

    @property
    def auc(self):
        """
        A convenience wrapper to rertrieve the auc of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.auc

    # ----------------------------------------------------------------

    def check(self, population_table, peripheral_tables=None):
        """
        Checks the validity of the data model.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.
            peripheral_tables (List[:class:`getml.data.DataFrame`] or dict):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders!
        """

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        temp = copy.deepcopy(self)

        # ------------------------------------------------------------

        temp._send()

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = temp.type + ".check"
        cmd["name_"] = temp.id

        cmd["peripheral_names_"] = [df.name for df in peripheral_tables]
        cmd["population_name_"] = population_table.name

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        print("Checking data model...")

        no_warnings = comm.recv_warnings(sock)

        if no_warnings:
            print("OK.")

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        temp.delete()

    # ------------------------------------------------------------

    @property
    def columns(self):
        """
        :class:`~getml.pipeline.Columns` object that
        can be used to handle the columns generated
        by the feature learners.
        """
        self._check_whether_fitted()
        return Columns(self.id, self.targets, self.peripheral)

    # ----------------------------------------------------------------

    @property
    def cross_entropy(self):
        """
        A convenience wrapper to rertrieve the cross entropy of the latest scoring
        run (the last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.cross_entropy

    # ----------------------------------------------------------------

    def delete(self):
        """
        Deletes the pipeline from the engine.

        Raises:
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.pipeline.Pipeline.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.pipeline.Pipeline.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.pipeline.Pipeline.validate`).

        Note:
            Caution: You can not undo this action!
        """
        self._check_whether_fitted()

        cmd = dict()
        cmd["type_"] = self.type + ".delete"
        cmd["name_"] = self.id
        cmd["mem_only_"] = False

        comm.send(cmd)

        self._id = NOT_FITTED

    # ------------------------------------------------------------

    def deploy(self, deploy):
        """Allows a fitted pipeline to be addressable via an HTTP request.
        See :ref:`deployment` for details.

        Args:
            deploy (bool): If :code:`True`, the deployment of the pipeline
                will be triggered.

        Raises:
            TypeError: If `deploy` is not of type bool.
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        if not isinstance(deploy, bool):
            raise TypeError("'deploy' must be of type bool")

        # ------------------------------------------------------------

        self.validate()

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".deploy"
        cmd["name_"] = self.id
        cmd["deploy_"] = deploy

        comm.send(cmd)

        self._save()

    # ------------------------------------------------------------

    @property
    def features(self):
        """
        :class:`~getml.pipeline.Features` object that
        can be used to handle the features generated
        by the feature learners.
        """
        self._check_whether_fitted()
        return Features(self.id, self.targets)

    # ------------------------------------------------------------

    def fit(self, population_table, peripheral_tables=None):
        """Trains the feature learning algorithms, feature selectors
        and predictors.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`getml.data.DataFrame`]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be passed in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the pipeline corresponding to the instance
                variable ``name`` could not be found on the engine or
                the pipeline could not be fitted.
            TypeError: If any input argument is not of proper type.
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).
        """

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self.check(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self._send()

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = self.type + ".fit"
        cmd["name_"] = self.id

        cmd["peripheral_names_"] = [df.name for df in peripheral_tables]
        cmd["population_name_"] = population_table.name

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        begin = time.time()

        msg = comm.log(sock)

        end = time.time()

        # ------------------------------------------------------------

        if "Trained" in msg:
            print()
            print(msg)
            _print_time_taken(begin, end, "Time taken: ")
        else:
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        self._save()

        # ------------------------------------------------------------

        return self.refresh()

    # ------------------------------------------------------------

    @property
    def fitted(self):
        """
        Whether the pipeline has already been fitted.
        """
        return self._id != NOT_FITTED

    # ------------------------------------------------------------

    def info(self):
        """
        Prints detailed information on the Pipeline.
        """

        info_str = """Data schema\n------------\n\n"""

        info_str += str(self.population)

        info_str += """\n\nPipeline steps\n--------------\n\n"""

        info_str += "1) Feature learners\n\n"

        feature_learners = [str(elem) for elem in self.feature_learners]

        info_str += "\n\n".join(feature_learners)

        info_str += "\n\n2) Feature selectors\n\n"

        feature_selectors = [str(elem) for elem in self.feature_selectors]

        info_str += "\n\n".join(feature_selectors)

        info_str += "\n\n3) Predictors\n\n"

        predictors = [str(elem) for elem in self.predictors]

        info_str += "\n\n".join(predictors)

        print(info_str)

    # ----------------------------------------------------------------

    @property
    def mae(self):
        """
        A convenience wrapper to rertrieve the mae of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.mae

    # ------------------------------------------------------------

    @property
    def metrics(self):
        """
        :class:`~getml.pipeline.Metrics` object that
        can be used to generate metrics like an ROC
        curve or a lift curve.
        """
        self._check_whether_fitted()
        return Metrics(self.id)

    # ------------------------------------------------------------

    @property
    def id(self):
        """
        ID of the pipeline. This is used to uniquely identify
        the pipeline on the engine.
        """
        return self._id

    # ------------------------------------------------------------

    @property
    def is_classification(self):
        """
        Whether the pipeline can used for classification problems.
        """
        return self._check_classification_or_regression()

    # ------------------------------------------------------------

    @property
    def is_regression(self):
        """
        Whether the pipeline can used for regression problems.
        """
        return not self.is_classification

    # ------------------------------------------------------------

    @property
    def name(self):
        """
        Returns the ID of the pipeline. The name property is
        kept for backward compatibility.
        """
        return self._id

    # ------------------------------------------------------------

    def predict(self, population_table, peripheral_tables=None, table_name=""):
        """Forecasts on new, unseen data using the trained ``predictor``.

        Returns the predictions generated by the pipeline based on
        `population_table` and `peripheral_tables` or writes them into
        a data base named `table_name`.

        Args:
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (
                Union[:class:`getml.data.DataFrame`, List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.
            table_name (str, optional):
                If not an empty string, the resulting predictions will
                be written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for further information.


        Raises:
            IOError: If the pipeline corresponding to the instance
                variable ``name`` could not be found on the engine or
                the pipeline could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set.
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Return:
            :class:`numpy.ndarray`:
                Resulting predictions provided in an array of the
                (number of rows in `population_table`, number of
                targets in `population_table`).

        Note:
            Only fitted pipelines
            (:meth:`~getml.pipeline.Pipeline.fit`) can be used for
            prediction.

        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        if not isinstance(table_name, str):
            raise TypeError("'table_name' must be of type str")

        # ------------------------------------------------------------

        self.validate()

        # ------------------------------------------------------------

        # Prepare the command for the getML engine.
        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that pipeline has
        # been found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        y_hat = self._transform(
            peripheral_tables,
            population_table,
            sock,
            predict=True,
            table_name=table_name,
        )

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

        # ------------------------------------------------------------

        return y_hat

    # ------------------------------------------------------------

    def refresh(self):
        """Reloads the pipeline from the engine.

        This discards all local changes you have made since the
        last time you called :meth:`~getml.pipeline.Pipeline.fit`.

        Raises:
            IOError:
                If the engine did not send a proper pipeline.

        Returns:
            :class:`~getml.pipeline.Pipeline`:
                Current instance
        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".refresh"
        cmd["name_"] = self.id

        sock = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        sock.close()

        if msg[0] != "{":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        json_obj = json.loads(msg)

        self._parse_json_obj(json_obj)

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    @property
    def rmse(self):
        """
        A convenience wrapper to rertrieve the rmse of the latest scoring run
        (the last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.rmse

    # ----------------------------------------------------------------

    @property
    def rsquared(self):
        """
        A convenience wrapper to rertrieve the rsquared of the latest scoring run
        (the last time `.score()` was called) on the pipeline.

        For programmatic access use `getml.pipeline.scores`.
        """
        return self.scores.rsquared

    # ----------------------------------------------------------------

    def score(self, population_table, peripheral_tables=None):
        """Calculates the performance of the ``predictor``.

        Returns different scores calculated on `population_table` and
        `peripheral_tables`.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.
            peripheral_tables (
                Union[:class:`getml.data.DataFrame`, List[:class:`getml.data.DataFrame`], dict]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the pipeline corresponding to the instance
                variable ``id`` could not be found on the engine or
                the pipeline could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set.
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Return:
            dict:

                Mapping of the name of the score (str) to the
                corresponding value (float).

                For regression problems the following scores are
                returned:

                * :const:`~getml.pipeline.scores.rmse`
                * :const:`~getml.pipeline.scores.mae`
                * :const:`~getml.pipeline.scores.rsquared`

                For classification problems the
                following scores are returned:

                * :const:`~getml.pipeline.scores.accuracy`
                * :const:`~getml.pipeline.scores.auc`
                * :const:`~getml.pipeline.scores.cross_entropy`

        Note:
            Only fitted pipelines
            (:meth:`~getml.pipeline.Pipeline.fit`) can be
            scored.
        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        # Prepare the command for the getml engine.
        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that pipeline has
        # been found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        self._transform(
            peripheral_tables, population_table, sock, predict=True, score=True
        )

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        if msg != "Success!":
            sock.close()
            comm.engine_exception_handler(msg)

        scores = comm.recv_string(sock)

        scores = json.loads(scores)

        # ------------------------------------------------------------

        self.refresh()

        self._save()

        # ------------------------------------------------------------

        return self.scores

    # ----------------------------------------------------------------

    @property
    def scores(self):
        """
        Contains all scores generated by :meth:`getml.pipeline.Pipeline.score`

        Returns:
            :class:`getml.pipeline.Scores`:
                A container that holds the scores for the pipeline.

        """
        self._check_whether_fitted()

        scores = self._make_score_history()

        latest = {score: self._get_latest_score(score) for score in _all_scores}

        return Scores(scores, latest)

    # ----------------------------------------------------------------

    @property
    def scored(self):
        """
        Whether the pipeline has been scored.
        """
        if self._scores is None:
            return False
        return len(self._scores) > 1

    # ----------------------------------------------------------------
    @property
    def targets(self):
        """
        Contains the names of the targets used for this pipeline.
        """
        self._check_whether_fitted()
        return copy.deepcopy(self._targets)

    # ----------------------------------------------------------------

    def transform(
        self, population_table, peripheral_tables=None, df_name="", table_name=""
    ):
        """Translates new data into the trained features.

        Transforms the data provided in `population_table` and
        `peripheral_tables` into features, which can be used to drive
        machine learning models. In addition to returning them as
        numerical array, this method is also able to return a
        :class:`getml.data.DataFrame` or write the results in a
        data base called `table_name`.

        Args:
            population_table (:class:`getml.data.DataFrame`):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (List[:class:`getml.data.DataFrame`]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders. A single
                DataFrame will be wrapped into a list internally.
            df_name (str, optional):
                If not an empty string, the resulting features will be
                written into a newly created DataFrame.
            table_name (str, optional):
                If not an empty string, the resulting features will be
                written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for further information.

        Raises:
            IOError: If the pipeline could not be found on the engine or
                the pipeline could not be fitted.
            TypeError: If any input argument is not of proper type.
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Returns:
            :class:`numpy.ndarray`:
                Resulting features provided in an array of the
                (number of rows in `population_table`, number of
                selected features).
            or :class:`getml.data.DataFrame`:
                A DataFrame containing the resulting features.

        Examples:
             By default, transform returns a :class:`numpy.ndarray`:
             .. code-block:: python
                my_features_array = pipe.transform()

             You can also export your features as :class:`getml.data.DataFrame`
             by providing the `df_name` argument:
             .. code-block:: python
                my_features_df = pipe.transform(df_name="my_features")

        Note:

            Only fitted pipelines
            (:meth:`~getml.pipeline.Pipeline.fit`) can transform
            data into features.
        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self.validate()

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        y_hat = self._transform(
            peripheral_tables,
            population_table,
            sock,
            df_name=df_name,
            table_name=table_name,
        )

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        if df_name != "":
            y_hat = data.DataFrame(name=df_name).refresh()

        # ------------------------------------------------------------

        return y_hat

    # ----------------------------------------------------------------

    def validate(self):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note:
            This method is triggered at the end of the __init__
            constructor and every time a function communicating with
            the getML engine - except
            :meth:`~getml.pipeline.Pipeline.refresh` - is called.
        """

        # ------------------------------------------------------------

        if not isinstance(self.id, str):
            raise TypeError("'name' must be of type str")

        if not isinstance(self.population, Placeholder):
            raise TypeError("'population' must be a getml.data.Placeholder or None.")

        if not _is_typed_list(self.peripheral, data.Placeholder):
            raise TypeError(
                "'peripheral' must be either a getml.data.Placeholder or a list of those"
            )

        if not _is_subclass_list(self.preprocessors, _Preprocessor):
            raise TypeError("'preprocessor' must be a list of _Preprocessor.")

        if not _is_subclass_list(self.feature_learners, _FeatureLearner):
            raise TypeError("'feature_learners' must be a list of _FeatureLearners.")

        if not _is_subclass_list(self.feature_selectors, _Predictor):
            raise TypeError(
                "'feature_selectors' must be a list of getml.predictors._Predictors."
            )

        if not _is_subclass_list(self.predictors, _Predictor):
            raise TypeError(
                "'predictors' must be a list of getml.predictors._Predictors."
            )

        if not isinstance(self.population, Placeholder):
            raise TypeError("'population' must be a getml.data.Placeholder or None.")

        if not isinstance(self.include_categorical, bool):
            raise TypeError("'include_categorical' must be a bool!")

        if not isinstance(self.share_selected_features, numbers.Real):
            raise TypeError("'share_selected_features' must be number!")

        if not _is_typed_list(self.tags, str):
            raise TypeError("'tags' must be a list of str.")

        # ------------------------------------------------------------

        if self.type != "Pipeline":
            raise ValueError("'type' must be 'Pipeline'")

        # ------------------------------------------------------------

        for kkey in self.__dict__:
            if kkey not in Pipeline._supported_params:
                raise KeyError(
                    """Instance variable ["""
                    + kkey
                    + """]
                       is not supported in Pipeline."""
                )

        # ------------------------------------------------------------

        for elem in self.feature_learners:
            elem.validate()

        for elem in self.feature_selectors:
            elem.validate()

        for elem in self.predictors:
            elem.validate()

        # ------------------------------------------------------------

        self._check_classification_or_regression()

        # ------------------------------------------------------------


class Tags(list):
    """
    A small lists-type class that allows to search for arbitrary substrings within its items.
    """

    def __contains__(self, substr):
        return any(substr in tag for tag in self)

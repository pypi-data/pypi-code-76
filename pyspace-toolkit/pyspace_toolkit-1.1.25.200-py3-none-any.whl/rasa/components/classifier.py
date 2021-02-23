# %%
import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type

import numpy as np
from scipy.sparse import csr_matrix

import rasa.utils.io as io_utils
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.classifiers import LABEL_RANKING_LENGTH
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import DENSE_FEATURE_NAMES, SPARSE_FEATURE_NAMES, TEXT
from rasa.nlu.featurizers.featurizer import sequence_to_sentence_features
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils

logger = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    import sklearn


class SklearnIntentClassifierExtended(IntentClassifier):
    """Intent classifier using the sklearn framework"""

    #     @classmethod
    #     def required_components(cls) -> List[Type[Component]]:
    #         return [DenseFeaturizer]

    #    defaults = {
    #         # C parameter of the svm - cross validation will select the best value
    #         "C": [1, 2, 5, 10, 20, 100],
    #         # gamma parameter of the svm
    #         "gamma": [0.1],
    #         # the kernels to use for the svm training - cross validation will
    #         # decide which one of them performs best
    #         "kernels": ["linear"],
    #         # We try to find a good number of cross folds to use during
    #         # intent training, this specifies the max number of folds
    #         "max_cross_validation_folds": 5,
    #         # Scoring function used for evaluating the hyper parameters
    #         # This can be a name or a function (cfr GridSearchCV doc for more info)
    #         "scoring_function": "f1_weighted",
    #    }

    defaults = {
        "prob_norm":False,
        "prob_norm_select_N_items": 5,
        "prob_norm_limit_X_times": 3,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        clf: "sklearn.calibration.CalibratedClassifierCV" = None,
        le: Optional["sklearn.preprocessing.LabelEncoder"] = None,
    ) -> None:
        """Construct a new intent classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        super().__init__(component_config)

        self.prob_norm = self.component_config["prob_norm"]
        self.prob_norm_select_N_items = self.component_config["prob_norm_select_N_items"]
        self.prob_norm_limit_X_times = self.component_config["prob_norm_limit_X_times"]

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    #     @classmethod
    #     def required_packages(cls) -> List[Text]:
    #         return ["sklearn"]

    def transform_labels_str2num(self, labels: List[Text]) -> np.ndarray:
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y: np.ndarray) -> np.ndarray:
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train the intent classifier on a data set."""

    #         num_threads = kwargs.get("num_threads", 1)

        labels = [e.get("intent") for e in training_data.intent_examples]

        if len(set(labels)) < 2:
            common_utils.raise_warning(
                "Can not train an intent classifier as there are not "
                "enough intents. Need at least 2 different intents. "
                "Skipping training of intent classifier.",
                docs=DOCS_URL_TRAINING_DATA_NLU,
            )
        else:
            y = self.transform_labels_str2num(labels)
            X = np.stack(
                [
    #                     np.concatenate(
    #                         [
    #                             sequence_to_sentence_features(
    #                                 example.get(DENSE_FEATURE_NAMES[TEXT])
    #                             ),
    #                             sequence_to_sentence_features(
    #                                 example.get(SPARSE_FEATURE_NAMES[TEXT])
    #                             )
    #                         ],axis=1          
    #                     )
                    sequence_to_sentence_features(
                        example.get(SPARSE_FEATURE_NAMES[TEXT]).toarray()
                    )
                    
                    for example in training_data.intent_examples
                ]
            )
            # reduce dimensionality
            X = np.reshape(X, (len(X), -1))
            X = csr_matrix(X)            
            
    #             # reduce dimensionality
    #             print(X.shape, type(X))
    #             logging.info(str(X.shape)+ ", " + str(type(X)))
    #             X = np.reshape(X, (len(X), -1))
    #             print(X.shape, type(X))
    #             logging.info(str(X.shape)+ ", " + str(type(X)))
    #             X = csr_matrix(X)
    #             print(X.shape, type(X))
    #             logging.info(str(X.shape)+ ", " + str(type(X)))
                
    #             temp = sequence_to_sentence_features(
    #                 training_data.intent_examples[0].get(SPARSE_FEATURE_NAMES[TEXT])
    #             )
    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))
    #             temp = temp.reshape(1, -1)
    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))
    #             temp = temp.tocsr()
    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))

                
                
                
    #             temp = sequence_to_sentence_features(
    #                 training_data.intent_examples[0].get(SPARSE_FEATURE_NAMES[TEXT]).toarray()
    #             )
                
    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))
    #             temp = temp.reshape(1, -1)
                    
    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))
    #             temp  = csr_matrix(temp)

    #             print(temp.shape, type(temp))
    #             logging.info(str(temp.shape)+ ", " + str(type(temp)))

                
                
    #             self.clf = self._create_classifier(num_threads, y)


            from sklearn.model_selection import StratifiedKFold
            from sklearn.calibration import CalibratedClassifierCV
            from sklearn.svm import LinearSVC
            
            self.clf = CalibratedClassifierCV(base_estimator=LinearSVC(random_state=0), cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0) )
            # GridSearcCV(SVM(kernel='linear'), )
            with warnings.catch_warnings():
                # sklearn raises lots of
                # "UndefinedMetricWarning: F - score is ill - defined"
                # if there are few intent examples, this is needed to prevent it
                warnings.simplefilter("ignore")
                self.clf.fit(X, y)

    #     def _num_cv_splits(self, y) -> int:
    #         folds = self.component_config["max_cross_validation_folds"]
    #         return max(2, min(folds, np.min(np.bincount(y)) // 5))

    #     def _create_classifier(
    #         self, num_threads: int, y
    #     ) -> "sklearn.model_selection.GridSearchCV":
    #         from sklearn.model_selection import GridSearchCV
    #         from sklearn.svm import SVC

    #         C = self.component_config["C"]
    #         kernels = self.component_config["kernels"]
    #         gamma = self.component_config["gamma"]
    #         # dirty str fix because sklearn is expecting
    #         # str not instance of basestr...
    #         tuned_parameters = [
    #             {"C": C, "gamma": gamma, "kernel": [str(k) for k in kernels]}
    #         ]

    #         # aim for 5 examples in each fold

    #         cv_splits = self._num_cv_splits(y)

    #         return GridSearchCV(
    #             SVC(C=1, probability=True, class_weight="balanced"),
    #             param_grid=tuned_parameters,
    #             n_jobs=num_threads,
    #             cv=cv_splits,
    #             scoring=self.component_config["scoring_function"],
    #             verbose=1,
    #             iid=False,
    #         )

    def process(self, message: Message, **kwargs: Any) -> None:
        """Return the most likely intent and its probability for a message."""

        if not self.clf:
            # component is either not trained or didn't
            # receive enough training data
            intent = None
            intent_ranking = []
        else:
            X = sequence_to_sentence_features(
                message.get(SPARSE_FEATURE_NAMES[TEXT]).toarray()
            ).reshape(1, -1)
            X = csr_matrix(X)
            
            # X = sequence_to_sentence_features(
            #     message.get(SPARSE_FEATURE_NAMES[TEXT])
            # ).reshape(1, -1)
            # X = X.tocsr()
            
            intent_ids, probabilities = self.predict(X)
            intents = self.transform_labels_num2str(np.ravel(intent_ids))
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            probabilities = probabilities.flatten()

            if intents.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(intents), list(probabilities)))[
                    :LABEL_RANKING_LENGTH
                ]

                intent = {"name": intents[0], "confidence": probabilities[0]}

                intent_ranking = [
                    {"name": intent_name, "confidence": score}
                    for intent_name, score in ranking
                ]
            else:
                intent = {"name": None, "confidence": 0.0}
                intent_ranking = []

        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def predict_prob(self, X: np.ndarray) -> np.ndarray:
        """Given a bow vector of an input text, predict the intent label.
        Return probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        probabilities = self.clf.predict_proba(X)

        ##########################################
        # probability normalization
        
        if self.prob_norm:

            probabilities = probabilities[0]

            sorted_indices = np.argsort(probabilities)[::-1]
            top_indices = sorted_indices[:self.prob_norm_select_N_items]
            other_indices = sorted_indices[self.prob_norm_select_N_items:]

            multiplier = min(1 / np.sum(probabilities[top_indices]), self.prob_norm_limit_X_times)

            probabilities[top_indices] = probabilities[top_indices] * multiplier
            remaining_ratio = 1 - np.sum(probabilities[top_indices])

            remaining_multiplier = remaining_ratio / np.sum(probabilities[other_indices])
            probabilities[other_indices] = probabilities[other_indices] * remaining_multiplier

            probabilities = probabilities.reshape(1, -1)
        ##########################################


        return probabilities

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Given a bow vector of an input text, predict most probable label.
        Return only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory."""

        classifier_file_name = file_name + "_classifier.pkl"
        encoder_file_name = file_name + "_encoder.pkl"
        if self.clf and self.le:
            
            import pickle
            with open(os.path.join(model_dir, classifier_file_name), 'wb') as f:
                pickle.dump(self.clf, f)
            # with open('../sahin_resources/datasets/bilmis/others/clsvm_test.pkl', 'rb') as f:
            #     clf_test = pickle.load(f)
            io_utils.json_pickle(
                os.path.join(model_dir, encoder_file_name), self.le.classes_
            )
            # io_utils.json_pickle(
            #     os.path.join(model_dir, classifier_file_name), self.clf
            # )
        return {"classifier": classifier_file_name, "encoder": encoder_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["SklearnIntentClassifierExtended"] = None,
        **kwargs: Any,
    ) -> "SklearnIntentClassifierExtended":
        from sklearn.preprocessing import LabelEncoder

        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        encoder_file = os.path.join(model_dir, meta.get("encoder"))

        if os.path.exists(classifier_file):
            
            import pickle
            # with open(os.path.join(model_dir, classifier_file_name), 'wb') as f:
            #     pickle.dump(self.clf, f)
            with open(classifier_file, 'rb') as f:
                classifier = pickle.load(f)
            # classifier = io_utils.json_unpickle(classifier_file)
            classes = io_utils.json_unpickle(encoder_file)
            encoder = LabelEncoder()
            encoder.classes_ = classes
            return cls(meta, classifier, encoder)
        else:
            return cls(meta)


class CalibratedClassifierLinearSVC(IntentClassifier):
    """Intent classifier using the sklearn framework"""

    defaults = {
        "prob_norm":False,
        "prob_norm_select_N_items": 5,
        "prob_norm_limit_X_times": 3,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        clf: "sklearn.calibration.CalibratedClassifierCV" = None,
        le: Optional["sklearn.preprocessing.LabelEncoder"] = None,
    ) -> None:
        """Construct a new intent classifier using the sklearn framework."""
        from sklearn.preprocessing import LabelEncoder

        super().__init__(component_config)

        self.prob_norm = self.component_config["prob_norm"]
        self.prob_norm_select_N_items = self.component_config["prob_norm_select_N_items"]
        self.prob_norm_limit_X_times = self.component_config["prob_norm_limit_X_times"]

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.clf = clf

    def transform_labels_str2num(self, labels: List[Text]) -> np.ndarray:
        """Transforms a list of strings into numeric label representation.
        :param labels: List of labels to convert to numeric representation"""

        return self.le.fit_transform(labels)

    def transform_labels_num2str(self, y: np.ndarray) -> np.ndarray:
        """Transforms a list of strings into numeric label representation.
        :param y: List of labels to convert to numeric representation"""

        return self.le.inverse_transform(y)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train the intent classifier on a data set."""

        labels = [e.get("intent") for e in training_data.intent_examples]

        if len(set(labels)) < 2:
            common_utils.raise_warning(
                "Can not train an intent classifier as there are not "
                "enough intents. Need at least 2 different intents. "
                "Skipping training of intent classifier.",
                docs=DOCS_URL_TRAINING_DATA_NLU,
            )
        else:
            y = self.transform_labels_str2num(labels)
            X = np.stack(
                [
                    sequence_to_sentence_features(
                        example.get(SPARSE_FEATURE_NAMES[TEXT]) #.toarray()
                    )
                    
                    for example in training_data.intent_examples
                ]
            )
            # reduce dimensionality
            X = np.reshape(X, (len(X), -1))
            X = csr_matrix(X)            
            


            from sklearn.model_selection import StratifiedKFold
            from sklearn.calibration import CalibratedClassifierCV
            from sklearn.svm import LinearSVC
            
            self.clf = CalibratedClassifierCV(base_estimator=LinearSVC(random_state=0), cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=0) )
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.clf.fit(X, y)

    def process(self, message: Message, **kwargs: Any) -> None:
        """Return the most likely intent and its probability for a message."""

        if not self.clf:
            intent = None
            intent_ranking = []
        else:
            X = sequence_to_sentence_features(
                message.get(SPARSE_FEATURE_NAMES[TEXT]).toarray()
            ).reshape(1, -1)
            X = csr_matrix(X)
            
            intent_ids, probabilities = self.predict(X)
            intents = self.transform_labels_num2str(np.ravel(intent_ids))
            # `predict` returns a matrix as it is supposed
            # to work for multiple examples as well, hence we need to flatten
            probabilities = probabilities.flatten()

            if intents.size > 0 and probabilities.size > 0:
                ranking = list(zip(list(intents), list(probabilities)))[
                    :LABEL_RANKING_LENGTH
                ]

                intent = {"name": intents[0], "confidence": probabilities[0]}

                intent_ranking = [
                    {"name": intent_name, "confidence": score}
                    for intent_name, score in ranking
                ]
            else:
                intent = {"name": None, "confidence": 0.0}
                intent_ranking = []

        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def predict_prob(self, X: np.ndarray) -> np.ndarray:
        """Given a bow vector of an input text, predict the intent label.
        Return probabilities for all labels.
        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""

        probabilities = self.clf.predict_proba(X)

        ##########################################
        # probability normalization
        
        if self.prob_norm:

            probabilities = probabilities[0]

            sorted_indices = np.argsort(probabilities)[::-1]
            top_indices = sorted_indices[:self.prob_norm_select_N_items]
            other_indices = sorted_indices[self.prob_norm_select_N_items:]

            multiplier = min(1 / np.sum(probabilities[top_indices]), self.prob_norm_limit_X_times)

            probabilities[top_indices] = probabilities[top_indices] * multiplier
            remaining_ratio = 1 - np.sum(probabilities[top_indices])

            remaining_multiplier = remaining_ratio / np.sum(probabilities[other_indices])
            probabilities[other_indices] = probabilities[other_indices] * remaining_multiplier

            probabilities = probabilities.reshape(1, -1)
        ##########################################


        return probabilities

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Given a bow vector of an input text, predict most probable label.
        Return only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        pred_result = self.predict_prob(X)
        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(pred_result, axis=1))
        return sorted_indices, pred_result[:, sorted_indices]

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory."""

        classifier_file_name = file_name + "_classifier.pkl"
        encoder_file_name = file_name + "_encoder.pkl"
        if self.clf and self.le:
            
            import pickle
            with open(os.path.join(model_dir, classifier_file_name), 'wb') as f:
                pickle.dump(self.clf, f)
            # with open('../sahin_resources/datasets/bilmis/others/clsvm_test.pkl', 'rb') as f:
            #     clf_test = pickle.load(f)
            io_utils.json_pickle(
                os.path.join(model_dir, encoder_file_name), self.le.classes_
            )
            # io_utils.json_pickle(
            #     os.path.join(model_dir, classifier_file_name), self.clf
            # )
        return {"classifier": classifier_file_name, "encoder": encoder_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["CalibratedClassifierLinearSVC"] = None,
        **kwargs: Any,
    ) -> "CalibratedClassifierLinearSVC":
        from sklearn.preprocessing import LabelEncoder

        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        encoder_file = os.path.join(model_dir, meta.get("encoder"))

        if os.path.exists(classifier_file):
            
            import pickle
            # with open(os.path.join(model_dir, classifier_file_name), 'wb') as f:
            #     pickle.dump(self.clf, f)
            with open(classifier_file, 'rb') as f:
                classifier = pickle.load(f)
            # classifier = io_utils.json_unpickle(classifier_file)
            classes = io_utils.json_unpickle(encoder_file)
            encoder = LabelEncoder()
            encoder.classes_ = classes
            return cls(meta, classifier, encoder)
        else:
            return cls(meta)

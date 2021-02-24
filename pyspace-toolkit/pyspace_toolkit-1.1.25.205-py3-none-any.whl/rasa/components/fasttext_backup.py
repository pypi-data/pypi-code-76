# %%
import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type

import numpy as np
from scipy.sparse import csr_matrix

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

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

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import fasttext

import pickle
from sklearn.model_selection import train_test_split

from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Embedding, Bidirectional, Dropout, LSTM, Dense, TimeDistributed
from tensorflow.keras.optimizers import Adam


import typing
from typing import Any, Optional, Text, Dict, List, Type
import fasttext
import numpy as np
import os
import io

from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.tokenizers.tokenizer import Tokenizer

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata
from rasa.nlu.constants import DENSE_FEATURE_NAMES, DENSE_FEATURIZABLE_ATTRIBUTES, TEXT

import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np

from rasa.nlu.constants import (
    TEXT,
    SPACY_DOCS,
    DENSE_FEATURE_NAMES,
    DENSE_FEATURIZABLE_ATTRIBUTES,
)

import string
import re
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

class FastText(IntentClassifier):
    # varying batch size
    # stratified batch
    # batch normalization layer
    # tqdm callback
    """
        unsupervised_default = {
            'model': "skipgram",
            'lr': 0.05,
            'dim': 100,
            'ws': 5,
            'epoch': 5,
            'minCount': 5,
            'minCountLabel': 0,
            'minn': 3,
            'maxn': 6,
            'neg': 5,
            'wordNgrams': 1,
            'loss': "ns",
            'bucket': 2000000,
            'thread': multiprocessing.cpu_count() - 1,
            'lrUpdateRate': 100,
            't': 1e-4,
            'label': "__label__",
            'verbose': 2,
            'pretrainedVectors': "",
            'seed': 0,
            'autotuneValidationFile': "",
            'autotuneMetric': "f1",
            'autotunePredictions': 1,
            'autotuneDuration': 60 * 5,  # 5 minutes
            'autotuneModelSize': ""
        }
    """
    defaults = {
        'epoch' : 50,
        'dim' : 300,
        'minn' : 2,
        'maxn' : 6,
        # 'lr' : 0.01,
        'wordNgrams': 1,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        clf = None,
        le = None,
    ) -> None:

        super().__init__(component_config)
        self.clf = clf
        self.le = le


    def generate_data(self, intent_examples, ):
        def write_fastext_dataset(X, y, path):
            # Create dataset
            with open(path, "w+", encoding='utf-8') as file:
                for text, label in zip(X, y):
                    file.write(f'__label__{label} {text}\n')
            
            # for idx, (text, label) in enumerate(zip(X, y)):
            #     if idx % 100 == 0:
            #         print()
            #         print(text)
            #         print(label)


        labels = [e.get("intent") for e in intent_examples]
        self.le = LabelEncoder()
        y = self.le.fit_transform(labels)

        texts = [message.text for message in intent_examples]
        write_fastext_dataset(texts, y, './fasttext_dataset.txt')
        
        return './fasttext_dataset.txt'

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        fasttext_dataset = self.generate_data(training_data.intent_examples,)
        fasttextparameters = {
            'epoch' : self.component_config["epoch"],
            'dim' : self.component_config["dim"],
            'minn' : self.component_config["minn"],
            'maxn' : self.component_config["maxn"],
            # 'lr' : self.component_config["lr"],
            'wordNgrams' : self.component_config["wordNgrams"],
        }
        print(fasttextparameters)
        self.clf = fasttext.train_supervised(input=fasttext_dataset, **fasttextparameters)
        print(self.clf.predict(['katildigim shell kampanyalari neler'], k=1))
        # pretrainedVectors=fasttext_pretrained_path, 
        
    def process(self, message: Message, **kwargs: Any) -> None:
        """Return the most likely intent and its probability for a message."""

        X = [message.text]
                
        intent_ids, probabilities = self.predict(X)
        intents = self.le.inverse_transform(np.ravel(intent_ids))

        probabilities = probabilities.flatten()

        if intents.size > 0 and probabilities.size > 0:
            ranking = list(zip(list(intents), list(probabilities)))[
                :LABEL_RANKING_LENGTH
            ]

            intent = {"name": intents[0], "confidence": float(probabilities[0])}

            intent_ranking = [
                {"name": intent_name, "confidence": float(score)}
                for intent_name, score in ranking
            ]
        else:
            intent = {"name": None, "confidence": 0.0}
            intent_ranking = []

        import json
        intent = json.loads(json.dumps(intent))
        intent_ranking = json.loads(json.dumps(intent_ranking))
        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Given a bow vector of an input text, predict most probable label.
        Return only the most likely label.
        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""

        sorted_indices, probabilities = self.clf.predict(X, k=-1)

        sorted_indices = [int(i.replace('__label__','')) for i in sorted_indices[0]]
        probabilities = probabilities[0]

        return sorted_indices, probabilities

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory."""

        classifier_file_name = file_name + "_classifier.bin"
        
        self.clf.save_model( os.path.join(model_dir, classifier_file_name) ) 

        temp = fasttext.load_model(os.path.join(model_dir, classifier_file_name))
        print(temp.predict(['katildigim shell kampanyalari neler'], k=1))

        preprocessing_file_name = file_name + "_preprocessing.pkl"
        preprocessing_variables = self.le.classes_
        
        with open(os.path.join(model_dir, preprocessing_file_name), 'wb') as f:
            pickle.dump(preprocessing_variables, f)

        return {"classifier": classifier_file_name, "preprocessing": preprocessing_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["FastText"] = None,
        **kwargs: Any,
    ) -> "FastText":
    
        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        preprocessing_file = os.path.join(model_dir, meta.get("preprocessing"))

        clf = fasttext.load_model(classifier_file)
        
        print(clf.predict(['katildigim shell kampanyalari neler'], k=1))
        with open(preprocessing_file, 'rb') as f:
            classes = pickle.load(f)

        le = LabelEncoder()
        le.classes_ = classes

        return cls(meta, clf, le,)


class FastTextEmbedding(DenseFeaturizer):

    defaults = {
        'epoch' : 50,
        'dim' : 300,
        'minn' : 2,
        'maxn' : 6,
        'wordNgrams': 1,
        'minCount': 1,

        'normalize_turkish': False,
        'normalize_lower': False,
        'normalize_digit': False,
        'fasttext_normalize_space_between_tokens': False,
        'fasttext_normalize_remove_punct': False,
    }

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None, clf=None, le=None) -> None:
        super().__init__(component_config)
        self.clf = clf
        self.le = le
        
    def preprocess_text(self, text):
        
        if self.component_config["normalize_turkish"]:
            text = xNormalizer.tr_normalize(text)
        if self.component_config["normalize_lower"]:
            text = text.lower()
        if self.component_config["normalize_digit"]:
            text = re.sub(f"""[0-9]""", 'D', text)
        
        return text

    def generate_data(self, intent_examples, ):
        print(1)

        def write_fastext_dataset(X, y, path):
            # Create dataset
            with open(path, "w+", encoding='utf-8') as file:
                for text, label in zip(X, y):
                    file.write(f'__label__{label} {text}\n')
            
        labels = [e.get("intent") for e in intent_examples]
        self.le = LabelEncoder()
        y = self.le.fit_transform(labels)


        if self.component_config["fasttext_normalize_space_between_tokens"]:
            texts = [[t.text for t in message.data["tokens"]] for message in intent_examples]

            if self.component_config["fasttext_normalize_remove_punct"]:
                def func_normalize_remove_punct(tokens):
                    output = []
                    for t in tokens: 
                        
                        temp = re.sub(fr"""[{re.escape(string.punctuation)}]""", '', t)
                        if temp != '':
                            output.append(temp)
                    return output
                texts = [func_normalize_remove_punct(tokens) for tokens in texts]

            texts = [" ".join(tokens) for tokens in texts]
        else:
            print(2)

            texts = [message.text for message in intent_examples]

            if self.component_config["fasttext_normalize_remove_punct"]:
                def func_normalize_remove_punct(text):
                    text = re.sub(fr"""(\s|^)[{string.punctuation}](\s|$)""", ' ', text).strip()
                    text = re.sub(fr"""[{re.escape(string.punctuation)}]""", '', text)
                    return text
                texts = [func_normalize_remove_punct(text) for text in texts]

        texts = [self.preprocess_text(text) for text in texts]
        print(len(texts))
        write_fastext_dataset(texts, y, './fasttext_dataset.txt')
        
        return './fasttext_dataset.txt'


    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        
        fasttext_dataset = self.generate_data(training_data.intent_examples,)
        fasttextparameters = {
            'epoch' : self.component_config["epoch"],
            'dim' : self.component_config["dim"],
            'minn' : self.component_config["minn"],
            'maxn' : self.component_config["maxn"],
            'wordNgrams' : self.component_config["wordNgrams"],
            'minCount': self.component_config["minCount"],
        }
        self.clf = fasttext.train_supervised(input=fasttext_dataset, **fasttextparameters)
        
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_features(example, attribute)

    def set_fasttext_features(self, message: Message, attribute: Text = TEXT):
        
        text_vector = self.clf.get_word_vector(self.preprocess_text(message.text))
        word_vectors = [
            self.clf.get_word_vector(self.preprocess_text(t.text))
            for t in message.data["tokens"]
            if t.text != "__CLS__"
        ]
        X = np.array(word_vectors + [text_vector])  # remember, we need one for __CLS__

        features = self._combine_with_existing_dense_features(
            message, additional_features=X, feature_name=DENSE_FEATURE_NAMES[attribute]
        )
        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def process(self, message: Message, **kwargs: Any) -> None:
        self.set_fasttext_features(message)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        
        classifier_file_name = file_name + "_classifier.bin"
        
        self.clf.save_model( os.path.join(model_dir, classifier_file_name) ) 

        preprocessing_file_name = file_name + "_preprocessing.pkl"
        preprocessing_variables = self.le.classes_
        
        with open(os.path.join(model_dir, preprocessing_file_name), 'wb') as f:
            pickle.dump(preprocessing_variables, f)

        return {"classifier": classifier_file_name, "preprocessing": preprocessing_file_name}


    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        preprocessing_file = os.path.join(model_dir, meta.get("preprocessing"))

        clf = fasttext.load_model(classifier_file)
        
        with open(preprocessing_file, 'rb') as f:
            classes = pickle.load(f)

        le = LabelEncoder()
        le.classes_ = classes

        return cls(meta, clf, le,)


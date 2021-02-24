import numpy as np
import typing
import logging
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import DenseFeaturizer
from rasa.nlu.utils.spacy_utils import SpacyNLP
from rasa.nlu.tokenizers.spacy_tokenizer import SpacyTokenizer
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.constants import (
    TEXT,
    SPACY_DOCS,
    DENSE_FEATURE_NAMES,
    DENSE_FEATURIZABLE_ATTRIBUTES,
)
from rasa.utils.tensorflow.constants import POOLING, MEAN_POOLING

if typing.TYPE_CHECKING:
    from spacy.tokens import Doc


logger = logging.getLogger(__name__)


class SpacyFeaturizer(DenseFeaturizer):

    defaults = {
        # Specify what pooling operation should be used to calculate the vector of
        # the CLS token. Available options: 'mean' and 'max'
        POOLING: MEAN_POOLING
    }

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None):
        super().__init__(component_config)

        self.pooling_operation = self.component_config[POOLING]

    def _features_for_doc(self, doc: "Doc") -> np.ndarray:
        """Feature vector for a single document / sentence / tokens."""
        return np.array([t.vector for t in doc])

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self._set_spacy_features(example, attribute)

    def get_doc(self, message: Message, attribute: Text) -> Any:
        return message.get(SPACY_DOCS[attribute])

    def process(self, message: Message, **kwargs: Any) -> None:
        self._set_spacy_features(message)

    def _set_spacy_features(self, message: Message, attribute: Text = TEXT) -> None:
        """Adds the spacy word vectors to the messages features."""
        doc = self.get_doc(message, attribute)

        if doc is None:
            return

        # in case an empty spaCy model was used, no vectors are present
        if doc.vocab.vectors_length == 0:
            logger.debug("No features present. You are using an empty spaCy model.")
            return

        features = self._features_for_doc(doc)

        cls_token_vec = self._calculate_cls_vector(features, self.pooling_operation)
        features = np.concatenate([features, cls_token_vec])

        features = self._combine_with_existing_dense_features(
            message, features, DENSE_FEATURE_NAMES[attribute]
        )
        message.set(DENSE_FEATURE_NAMES[attribute], features)


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

class FastTextFeaturizer(DenseFeaturizer):
    """A new component"""

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""
        return [Tokenizer]

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["fasttext"]

    defaults = {"file": None, "cache_dir": None}
    language_list = []

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        path = os.path.join(component_config["cache_dir"], component_config["file"])
        self.model = fasttext.load_model(path)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_features(example, attribute)

    def set_fasttext_features(self, message: Message, attribute: Text = TEXT):
        text_vector = self.model.get_word_vector(message.text)
        word_vectors = [
            self.model.get_word_vector(t.text)
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
        pass

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

        if cached_component:
            return cached_component
        else:
            return cls(meta)


class FastTextFeaturizerV2(DenseFeaturizer):
    """A new component"""

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""
        return [Tokenizer]

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["fasttext"]

    defaults = {"file": None, "cache_dir": None}
    language_list = []

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.path = os.path.join(component_config["cache_dir"], component_config["file"])
        self.model = False

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        if not self.model:
            self.model = fasttext.load_model(self.path)
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_features(example, attribute)

    def set_fasttext_features(self, message: Message, attribute: Text = TEXT):
        text_vector = self.model.get_word_vector(message.text)
        word_vectors = [
            self.model.get_word_vector(t.text)
            for t in message.data["tokens"]
            if t.text != "__CLS__"
        ]
        X = np.array(word_vectors + [text_vector])  # remember, we need one for __CLS__

        features = self._combine_with_existing_dense_features(
            message, additional_features=X, feature_name=DENSE_FEATURE_NAMES[attribute]
        )
        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def process(self, message: Message, **kwargs: Any) -> None:
        if not self.model:
            self.model = fasttext.load_model(self.path)
        self.set_fasttext_features(message)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        pass

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

        if cached_component:
            return cached_component
        else:
            return cls(meta)

class FastTextFeaturizerV3(DenseFeaturizer):
    """A new component"""

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""
        return [Tokenizer]

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["fasttext"]

    defaults = {"file": None, "cache_dir": None}
    language_list = []

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.path = os.path.join(component_config["cache_dir"], component_config["file"])
        self.model = False

    @staticmethod
    def load_vectors(fname):
        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        data = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        if not self.model:
            self.model = self.load_vectors(self.path)
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_fasttext_features(example, attribute)

    def set_fasttext_features(self, message: Message, attribute: Text = TEXT):
        text_vector = self.model[message.text] if message.text in self.model else self.model["_SP"]
        word_vectors = [
            self.model[t.text] if t.text in self.model else self.model["_SP"]
            for t in message.data["tokens"]
            if t.text != "__CLS__"
        ]
        X = np.array(word_vectors + [text_vector])  # remember, we need one for __CLS__

        features = self._combine_with_existing_dense_features(
            message, additional_features=X, feature_name=DENSE_FEATURE_NAMES[attribute]
        )
        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def process(self, message: Message, **kwargs: Any) -> None:
        if not self.model:
            self.model = self.load_vectors(self.path)
        self.set_fasttext_features(message)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        pass

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

        if cached_component:
            return cached_component
        else:
            return cls(meta)


class EmbeddingFeaturizer(DenseFeaturizer):

    defaults = {"emb_file": None, "word_index_file": None}

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        embedding_matrix = self.component_config["emb_file"]
        word_index = self.component_config["word_index_file"]
        
        with open(embedding_matrix, 'rb') as f:
            embedding_matrix = pickle.load(f)

        with open(word_index, 'rb') as f:
            word_index = pickle.load(f)

        #vocab = list(enumerate(vocab))
        #vocab = {w:i for i,w in vocab}

        self.embedding_matrix = embedding_matrix
        self.word_index = word_index

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        for example in training_data.intent_examples:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self.set_embedding_features(example, attribute)

    def get_word_vector(self, word):

        if word in self.word_index:
            return self.embedding_matrix[self.word_index[word]]
        else:
            return np.zeros(self.embedding_matrix.shape[1])


    def set_embedding_features(self, message: Message, attribute: Text = TEXT):
        text_vector = self.get_word_vector(message.text)
        word_vectors = [
            self.get_word_vector(t.text)
            for t in message.data["tokens"]
            if t.text != "__CLS__"
        ]
        X = np.array(word_vectors + [text_vector])  # remember, we need one for __CLS__

        features = self._combine_with_existing_dense_features(
            message, additional_features=X, feature_name=DENSE_FEATURE_NAMES[attribute]
        )
        message.set(DENSE_FEATURE_NAMES[attribute], features)

    def process(self, message: Message, **kwargs: Any) -> None:
        self.set_embedding_features(message)

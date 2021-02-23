
from typing import Any, Dict, List, Optional, Text, Tuple, Union, Type, NamedTuple

import tensorflow as tf

from rasa.nlu.constants import INTENT
from rasa.utils.tensorflow.constants import ENTITY_RECOGNITION
from rasa.nlu.training_data import TrainingData
from rasa.nlu.training_data import Message
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.classifiers.diet_classifier import DIETClassifier
from rasa.nlu.featurizers.sparse_featurizer.count_vectors_featurizer import CountVectorsFeaturizer

from rasa.nlu.constants import (
    INTENT,
    TEXT,
    ENTITIES,
    NO_ENTITY_TAG,
    TOKENS_NAMES,
    ENTITY_ATTRIBUTE_TYPE,
    ENTITY_ATTRIBUTE_GROUP,
    ENTITY_ATTRIBUTE_ROLE,
)

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


class CountVectorsFeaturizerExtended(CountVectorsFeaturizer):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
    
        super().train(training_data, config, **kwargs)

        print(self.vectorizers[TEXT].get_feature_names())
        print(training_data.training_examples[-1].get(SPARSE_FEATURE_NAMES[TEXT]))



        
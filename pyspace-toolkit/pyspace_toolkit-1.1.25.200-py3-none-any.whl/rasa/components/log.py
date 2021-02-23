
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig

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

class Log(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        sparse_features = training_data.training_examples[0].get(SPARSE_FEATURE_NAMES[TEXT])
        
        if str(type(sparse_features)) != str(type(None)):
            print(sparse_features.shape)
            
        elif str(type(sparse_features)) == str(type(None)):
            print(sparse_features)
        


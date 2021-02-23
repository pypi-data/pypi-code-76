import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

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

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

import copy
import re



class BatchInputSeparator(Component):

    def process(self, message: Message, **kwargs: Any) -> None:
        batch = message.text.split('###')
        batch = [Message(m) for m in batch]

        message.set('batch', batch)

class BatchOutputFormatter(Component):

    def process(self, message: Message, **kwargs: Any) -> None:

        # output = self.default_output_attributes()
        # output.update(message.as_dict(only_output_properties=only_output_properties))
        
        batch = message.get('batch')
        message.set('batch', [message.as_dict(only_output_properties=True) for message in batch])



class BatchProcessorTemplate(Component):

    def process(self, message: Message, **kwargs: Any) -> None:

        batch = message.get('batch')

        for message in batch:
            super().process(message)
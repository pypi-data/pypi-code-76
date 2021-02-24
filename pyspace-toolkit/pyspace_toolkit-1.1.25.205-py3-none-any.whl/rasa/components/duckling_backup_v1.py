
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

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


import re
import string

from rasa.nlu.extractors.duckling_http_extractor import DucklingHTTPExtractor


class DucklingExtractor(DucklingHTTPExtractor):

    def __init__(
            self,
            component_config: Optional[Dict[Text, Any]] = None,
            language: Optional[Text] = None,
    ) -> None:
        super().__init__(component_config)
        self.component_config['url'] = 'http://51.124.94.195:8000'
        
        
    def process(self, message: Message, **kwargs: Any):

        super().process(message, **kwargs)
        print(message.get("entities", []))
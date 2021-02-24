
# %%
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
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

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.nlp.task.date_extractor import DateParser

# %%
import copy
import pickle

from rasa.core.domain import Domain
from pathlib import Path

class IntentAndResponseMapper(Component):
    defaults = {
        'folder_name' : '/tmp',
        'file_name' : 'domain.yml',
        'apply_in_train_time': False,
        'intent_delimiter': '.',
    }

    def __init__(self, component_config: Dict[Text, Any] = None, response_dict=None) -> None:
        super(IntentAndResponseMapper, self).__init__(component_config)
        self.response_dict = response_dict



    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):


        folder_name = self.component_config['folder_name']
        file_name = self.component_config['file_name']
        
        domain_file_path = sorted(list(Path(folder_name).rglob(file_name)), key=lambda x: x.stat().st_ctime, reverse=True)[0].absolute().as_posix()
        domain = Domain.empty()
        domain = Domain.load(domain_file_path)
        domain = domain.as_dict()
        responses = domain['responses']
        
        self.response_dict = {}
        for k in responses:
            self.response_dict[k.replace('utter_group_', '')] = [r['text'] for r in responses[k]]
        
        if self.component_config["apply_in_train_time"]:
            for message in training_data.training_examples:
                pass

    
    def process(self, message: Message, **kwargs: Any) -> None:
        dl = self.component_config['intent_delimiter']
        intent = message.get(INTENT)
        
        if isinstance(intent, dict):
            if dl in intent['name'] and intent['name'] in self.response_dict:
                retrieval_intent = intent['name'].split(dl, 1)[0]
                
                
                message.set(INTENT, {'name': retrieval_intent, 'confidence': intent['confidence']})
                message.set('response_selector', {retrieval_intent: {
                    'response': {'name': self.response_dict[intent['name']], 'confidence': intent['confidence']},
                    'full_retrieval_intent': intent['name'],
                    }})

        elif isinstance(intent, str):
            pass


    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        
        response_dict_file_name = file_name + "_response_dict.pkl"
        
        with open(os.path.join(model_dir, response_dict_file_name), 'wb') as f:
            pickle.dump(self.response_dict, f)

        return {"response_dict": response_dict_file_name}

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

        response_dict_file = os.path.join(model_dir, meta.get("response_dict"))

        with open(response_dict_file, 'rb') as f:
            response_dict = pickle.load(f)

        return cls(meta, clf, response_dict,)


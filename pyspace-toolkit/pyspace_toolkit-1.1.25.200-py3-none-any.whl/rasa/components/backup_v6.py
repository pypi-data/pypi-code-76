# %%
# %% [markdown]
# https://rasa.com/docs/rasa/api/custom-nlu-components/
# If you create a custom tokenizer you should implement the methods of rasa.nlu.tokenizers.tokenizer.Tokenizer. The train and process methods are already implemented and you simply need to overwrite the tokenize method. train and process will automatically add a special token __CLS__ to the end of list of tokens, which is needed further down the pipeline.

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

# %%
import copy
import pickle

import numpy as np
import scipy.sparse

import stanza

# %%


class EntityManager(Component):

    defaults = {
        "priority_config": {},
    }

    def __init__(
        self,
        component_config: Dict[Text, Any] = None,
        priority_config: Any = None,
    ) -> None:
        # super(EntityManager, self).__init__(component_config)
        super().__init__(component_config)

        print('entity manager init component config')
        print(self.component_config["priority_config"])
        
        print('entity manager init parameter')
        print(priority_config)
        if priority_config:
            self.priority_config = priority_config
        else:
            self.priority_config = self.component_config["priority_config"]
            self.priority_config = [self.priority_config[i].split('___',1) for i in sorted (self.priority_config.keys())]
        
        print('entity manager init')
        print(self.priority_config)

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        print('process entity manager')

        if not self.priority_config:
            print('priority config is none')
            return

        entities = message.get("entities", [])

        entities_updated = copy.deepcopy(entities)
        
        
        temp = []
        for priority_i in self.priority_config:
            for entity in entities_updated:

                if [entity['extractor'], entity['entity']] == priority_i:
                    temp.append(entity)
                
        entities_updated = temp
        temp = []


        temp = []
        tempspan = []
        for entity in entities_updated:
            if not (entity['start'] in tempspan or entity['end'] in tempspan):
                temp.append(entity)
                tempspan.append(entity['start'])
                tempspan.append(entity['end'])

        entities_updated = temp
        temp = []

        #for entity in entities_updated:
        #    entity['entity'] = "EntityManager" + entity['entity']
        
        message.set("entities", entities_updated, add_to_output=True)

        

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        priority_config_file_name = file_name + "_priority_config.pkl"
        print(self.priority_config)
        with open(os.path.join(model_dir, priority_config_file_name), 'wb') as f:
            pickle.dump(self.priority_config, f)

        return {"priority_config_file_name": priority_config_file_name}

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional[Metadata] = None,
            cached_component: Optional["EntityManager"] = None,
            **kwargs: Any
    ) -> "EntityManager":

        priority_config_file_name = meta.get("priority_config_file_name")
        priority_config_file = os.path.join(model_dir, priority_config_file_name)

        with open(priority_config_file, 'rb') as f:
            priority_config = pickle.load(f)
        print('entity manager load')
        print(priority_config)
        return cls(meta, priority_config)





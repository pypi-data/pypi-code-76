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

class TrainingDataManager:

    ## TODO : Deprecated. Delete following method. Use BackupIntent, RenameIntents, RecoverIntent.
    @staticmethod
    def apply_grouped_labels(training_data, intent_groups, intent_groups_prefix):
        
        raw_intents = [message.get(INTENT) for message in training_data.training_examples]

        for message in training_data.training_examples:
            intent = message.get(INTENT)
            for idx, group_i in enumerate(intent_groups):
                if intent in group_i:
                    if len(group_i) != 1:
                        message.set(INTENT, f'{intent_groups_prefix}{idx}')
                    break

        return raw_intents

    ## TODO : Deprecated. Delete following method. Use BackupIntent, RenameIntents, RecoverIntent.
    @staticmethod
    def recover_original_labels(training_data, raw_intents):
        for message, raw_intent in zip(training_data.training_examples, raw_intents):
            message.set(INTENT, raw_intent)

    @staticmethod
    def select_intents(training_data, info, mode, ):
        if mode=='select':
            filter_intents = info
        elif mode=='exclude':
            filter_intents = TrainingDataManager.generate_filter_intents_by_exclude_intents(training_data, info)
        elif mode=='regex':
            filter_intents = TrainingDataManager.generate_filter_intents_by_regex(training_data, info)
        else:
            assert 'Partition mode is not allowed.' == 0
        return filter_intents

    @staticmethod
    def rename_selected_intents(training_data, selected_intents, rename_name):
        for message in training_data.training_examples:
            intent = message.get(INTENT)
            if intent in selected_intents:
                message.set(INTENT, rename_name)

    @staticmethod
    def rename_intents_with_regex(training_data, regex_pattern, replace_pattern):
        for message in training_data.training_examples:
            intent = message.get(INTENT)
            updated_intent_name = re.sub(regex_pattern, replace_pattern, intent)
            message.set(INTENT, updated_intent_name)

    @staticmethod
    def filter_trainingdata(training_data, filter_intents):
        return [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        
    @staticmethod
    def generate_filter_intents_by_regex(training_data, regex=''):
        
        # exclude pattern
        # '^(account_tr|bill_payment_tr)$'
        # '^((?!account_tr).)*$'
        # '^((?!(badword|one)).)*$'

        filter_intents = []
        all_intents = list(set([e.get(INTENT) for e in training_data.training_examples]))
        for intent in all_intents:
            if re.findall(regex, intent):
                filter_intents.append(intent)

        return filter_intents

    @staticmethod
    def generate_filter_intents_by_exclude_intents(training_data, exclude_intents=[]):
        filter_intents = []
        all_intents = list(set([e.get(INTENT) for e in training_data.training_examples]))
        for intent in all_intents:
            if intent not in exclude_intents:
                filter_intents.append(intent)

        return filter_intents
    
############################################################
############################################################



############################################################
############################################################

class BackupIntent(Component):
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        for example in training_data.training_examples:
            example.set(f"backup_intent", example.get(INTENT))

class RecoverIntent(Component):
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        for example in training_data.training_examples:
            example.set(INTENT, example.get(f"backup_intent"))

class BackupData(Component):
    defaults = {
        "deepcopy": False,
    }
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        if self.component_config["deepcopy"]:
            training_data.backup_data = copy.deepcopy(training_data.training_examples)
        else:
            training_data.backup_data = training_data.training_examples

class RecoverData(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        training_data.training_examples = training_data.backup_data

class BackupFeatures(Component):

    def backup_features(self, message):
        for feature in self.component_config["features"]:
            message.set(f"backup_{feature}", message.get(feature))

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.backup_features(message)

    def process(self, message: Message, **kwargs: Any) -> None:
        self.backup_features(message)

class RecoverFeatures(Component):

    def recover_features(self, message,):
        for feature in self.component_config["features"]:
            message.set(feature, message.get(f"backup_{feature}"))
            if feature == 'text':
                message.text = message.get(f"backup_{feature}")

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        for message in training_data.training_examples:
            self.recover_features(message)

    def process(self, message: Message, **kwargs: Any) -> None:
        self.recover_features(message)

############################################################
############################################################

class RenameSelectedIntents(Component):
    
    defaults = {
        "rename_intents":[],
        "rename_mode": 'select', # regex, 
        "rename_name": 'renamed',
    }
    
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        selected_intents = TrainingDataManager.select_intents(training_data, self.component_config["rename_intents"], self.component_config["rename_mode"], )
        TrainingDataManager.rename_selected_intents(training_data, selected_intents, self.component_config["rename_name"])

class RenameIntentsWithRegex(Component):
    
    defaults = {
        "rename_regex": '',
        "rename_name": 'renamed',
    }
    
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        TrainingDataManager.rename_intents_with_regex(training_data, self.component_config["rename_regex"], self.component_config["rename_name"])

############################################################
############################################################

## TODO : Deprecated. Remove this class. Use LoadPartition.
class LoadData(Component):
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        dataset = self.component_config["partition_name"]
        training_data.training_examples = getattr(training_data, dataset)

class LoadPartition(Component):
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        training_data.training_examples = getattr(training_data, self.component_config["partition_name"])
        
class PartitionData(Component):

    defaults = {
        "partition_intents":[],
        "partition_mode": 'select', # exclude, regex
        "partition_name": 'partition',
    }

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        assert self.component_config["partition_name"] not in ['training_examples', 'backup_data']

        filter_intents = TrainingDataManager.select_intents(training_data, self.component_config["partition_intents"], self.component_config["partition_mode"], )
        partition_training_examples = TrainingDataManager.filter_trainingdata(training_data, filter_intents)

        setattr(training_data, self.component_config["partition_name"], partition_training_examples)

############################################################
############################################################
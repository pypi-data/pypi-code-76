import logging
from collections import defaultdict
from pathlib import Path

import copy

import numpy as np
import os
import scipy.sparse
import tensorflow as tf
import tensorflow_addons as tfa

from typing import Any, Dict, List, Optional, Text, Tuple, Union, Type, NamedTuple

import rasa.utils.common as common_utils
import rasa.utils.io as io_utils
import rasa.nlu.utils.bilou_utils as bilou_utils
from rasa.nlu.featurizers.featurizer import Featurizer
from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.test import determine_token_labels
from rasa.nlu.classifiers import LABEL_RANKING_LENGTH
from rasa.utils import train_utils
from rasa.utils.tensorflow import layers
from rasa.utils.tensorflow.transformer import TransformerEncoder
from rasa.utils.tensorflow.models import RasaModel
from rasa.utils.tensorflow.model_data import RasaModelData, FeatureSignature
from rasa.nlu.constants import (
    INTENT,
    TEXT,
    ENTITIES,
    NO_ENTITY_TAG,
    SPARSE_FEATURE_NAMES,
    DENSE_FEATURE_NAMES,
    TOKENS_NAMES,
    ENTITY_ATTRIBUTE_TYPE,
    ENTITY_ATTRIBUTE_GROUP,
    ENTITY_ATTRIBUTE_ROLE,
)
from rasa.nlu.config import RasaNLUModelConfig, InvalidConfigError
from rasa.nlu.training_data import TrainingData
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message
from rasa.utils.tensorflow.constants import (
    LABEL,
    HIDDEN_LAYERS_SIZES,
    SHARE_HIDDEN_LAYERS,
    TRANSFORMER_SIZE,
    NUM_TRANSFORMER_LAYERS,
    NUM_HEADS,
    BATCH_SIZES,
    BATCH_STRATEGY,
    EPOCHS,
    RANDOM_SEED,
    LEARNING_RATE,
    DENSE_DIMENSION,
    RANKING_LENGTH,
    LOSS_TYPE,
    SIMILARITY_TYPE,
    NUM_NEG,
    SPARSE_INPUT_DROPOUT,
    DENSE_INPUT_DROPOUT,
    MASKED_LM,
    ENTITY_RECOGNITION,
    TENSORBOARD_LOG_DIR,
    INTENT_CLASSIFICATION,
    EVAL_NUM_EXAMPLES,
    EVAL_NUM_EPOCHS,
    UNIDIRECTIONAL_ENCODER,
    DROP_RATE,
    DROP_RATE_ATTENTION,
    WEIGHT_SPARSITY,
    NEGATIVE_MARGIN_SCALE,
    REGULARIZATION_CONSTANT,
    SCALE_LOSS,
    USE_MAX_NEG_SIM,
    MAX_NEG_SIM,
    MAX_POS_SIM,
    EMBEDDING_DIMENSION,
    BILOU_FLAG,
    KEY_RELATIVE_ATTENTION,
    VALUE_RELATIVE_ATTENTION,
    MAX_RELATIVE_POSITION,
    SOFTMAX,
    AUTO,
    BALANCED,
    TENSORBOARD_LOG_LEVEL,
)


TEXT_FEATURES = f"{TEXT}_features"
LABEL_FEATURES = f"{LABEL}_features"
LABEL_IDS = f"{LABEL}_ids"
TAG_IDS = "tag_ids"
TEXT_SEQ_LENGTH = f"{TEXT}_lengths"
LABEL_SEQ_LENGTH = f"{LABEL}_lengths"

POSSIBLE_TAGS = [ENTITY_ATTRIBUTE_TYPE, ENTITY_ATTRIBUTE_ROLE, ENTITY_ATTRIBUTE_GROUP]


from typing import Any, Dict, List, Optional, Text, Tuple, Union, Type, NamedTuple

import tensorflow as tf

from rasa.nlu.constants import INTENT
from rasa.utils.tensorflow.constants import ENTITY_RECOGNITION
from rasa.nlu.training_data import TrainingData
from rasa.nlu.training_data import Message
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.classifiers.diet_classifier import DIETClassifier

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

class DIETClassifierExtended(DIETClassifier):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
    
        ## FILTER START
        intent_filters = self.component_config['intent_filters']
        print(f'Filter intents : {intent_filters}')
        
        if intent_filters:
            backup_training_data_training_examples = training_data.training_examples
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in intent_filters]
            training_data.training_examples = filtered_training_examples

            print(f'    All example size : {len(backup_training_data_training_examples)}')
            print(f'    Filtered example size : {len(filtered_training_examples)}')
        ## FILTER END

        super().train(training_data, config, **kwargs)
        
        ## FILTER RECOVER START
        if intent_filters:
            training_data.training_examples = backup_training_data_training_examples

        ## FILTER RECOVER END

        ## GET ENTITY PREDICTIONS
        
        if self.component_config[ENTITY_RECOGNITION]:
            print('Predict entities for normalization.')
            prediction_batch_size = self.component_config['prediction_batch_size'] if 'prediction_batch_size' in self.component_config else 256
            print(f'  Number of batches to be executed : {len(training_data.training_examples)//prediction_batch_size +1}')
            print_example_count = self.component_config['print_example_count'] if 'print_example_count' in self.component_config else 0
            
            for i in range(len(training_data.training_examples)//prediction_batch_size +1):
                if i == len(training_data.training_examples)//prediction_batch_size:
                    print(f'  Last batch. Batch idx : {i}')
                elif i % 20 == 0:
                    print(f'  Batch idx : {i}')
                

                batch_data = training_data.training_examples[ i*prediction_batch_size: (i+1)*prediction_batch_size ]
                model_data = self._create_model_data(batch_data, training=False)
                batch_in = model_data.prepare_batch()
                out = self.model.batch_predict(batch_in)

                for k in out:
                    out[k] = out[k].numpy()

                for j, message in enumerate(batch_data):
                    outj = {k:tf.constant([out[k][j,:]]) for k in out}

                    # approach 1
                    ## entities = self._predict_entities(outj, message)
                    # approach 2
                    predict_out = outj

                    ## rasa 1.10.10
                    predicted_tags = self._entity_label_to_tags(predict_out)
                    entities = self.convert_predictions_into_entities(message.text, message.get(TOKENS_NAMES[TEXT], []), predicted_tags)
                    ## rasa 2.0.x
                    #predicted_tags, confidence_values = self._entity_label_to_tags(outj)
                    #entities = self.convert_predictions_into_entities(message.text, message.get(TOKENS_NAMES[TEXT], []), predicted_tags, confidence_values, )
                    # rasa end

                    entities = self.add_extractor_name(entities)
                    # entities = message.get(ENTITIES, []) + entities
                    # approach end

                    message.set('norm_ent', entities, )

                    if print_example_count != 0:
                        
                        # out = self._predict(message)
                        temp_model_data = self._create_model_data([message], training=False)
                        temp_out = self.model.predict(temp_model_data)
                        temp_entities = self._predict_entities(temp_out, message)

                        if entities != []:
                            print_example_count -= 1

                            print(message.text)
                            print()

                            print({k:outj[k].numpy() for k in outj})
                            print({k:temp_out[k].numpy() for k in temp_out})
                            print()

                            print(entities)
                            print(temp_entities)
                            print()


class PriorDIETClassifier(DIETClassifier):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
    
        ## FILTER START
        prior_groups = self.component_config['prior_groups']
        print(f'Prior groups : {prior_groups}')
        
        backup_training_data_training_examples = copy.deepcopy(training_data.training_examples)

        for message in training_data.training_examples:
            intent = message.get(INTENT)

            for idx, group_i in enumerate(prior_groups):
                if intent in group_i:
                    message.set(INTENT, f'prior_group_{idx}')
                    break

        ## FILTER END

        super().train(training_data, config, **kwargs)
        
        ## FILTER RECOVER START

        training_data.training_examples = backup_training_data_training_examples


    def process(self, message: Message, **kwargs: Any) -> None:
        
        super().process(message, **kwargs)

        intent = message.get(INTENT)
        message.set('prior_intent', intent)


class PriorDIETClassifierExtended(DIETClassifier):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        # del training_data._lazy_intent_examples
        
        ## FILTER START

        intent_filters = self.component_config['prior_group']
        print(f'Filter intents : {intent_filters}')
        
        if intent_filters:
            backup_training_data_training_examples = training_data.training_examples
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in intent_filters]
            training_data.training_examples = filtered_training_examples

            print(f'    All example size : {len(backup_training_data_training_examples)}')
            print(f'    Filtered example size : {len(filtered_training_examples)}')

        
        ## FILTER END

        super().train(training_data, config, **kwargs)
        
        ## FILTER RECOVER START
        if intent_filters:
            training_data.training_examples = backup_training_data_training_examples

        ## FILTER RECOVER END

    def process(self, message: Message, **kwargs: Any) -> None:
        
        prior_group_name = self.component_config['prior_group_name']
        prior_intent = message.get('prior_intent')['name']
        
        if prior_intent == prior_group_name:
            super().process(message, **kwargs)

    @staticmethod
    def _label_id_index_mapping(
        training_data: TrainingData, attribute: Text
    ) -> Dict[Text, int]:
        """Create label_id dictionary."""

        distinct_label_ids = {
            example.get(attribute) for example in training_data.training_examples
        } - {None}
        return {
            label_id: idx for idx, label_id in enumerate(sorted(distinct_label_ids))
        }

    def _create_label_data(
        self,
        training_data: TrainingData,
        label_id_dict: Dict[Text, int],
        attribute: Text,
    ) -> RasaModelData:
        """Create matrix with label_ids encoded in rows as bag of words.
        Find a training example for each label and get the encoded features
        from the corresponding Message object.
        If the features are already computed, fetch them from the message object
        else compute a one hot encoding for the label as the feature vector.
        """

        # Collect one example for each label
        labels_idx_examples = []
        for label_name, idx in label_id_dict.items():
            label_example = self._find_example_for_label(
                label_name, training_data.training_examples, attribute
            )
            labels_idx_examples.append((idx, label_example))

        # Sort the list of tuples based on label_idx
        labels_idx_examples = sorted(labels_idx_examples, key=lambda x: x[0])
        labels_example = [example for (_, example) in labels_idx_examples]

        # Collect features, precomputed if they exist, else compute on the fly
        if self._check_labels_features_exist(labels_example, attribute):
            features = self._extract_labels_precomputed_features(
                labels_example, attribute
            )
        else:
            features = self._compute_default_label_features(labels_example)

        label_data = RasaModelData()
        label_data.add_features(LABEL_FEATURES, features)

        label_ids = np.array([idx for (idx, _) in labels_idx_examples])
        # explicitly add last dimension to label_ids
        # to track correctly dynamic sequences
        label_data.add_features(LABEL_IDS, [np.expand_dims(label_ids, -1)])

        label_data.add_lengths(LABEL_SEQ_LENGTH, LABEL_FEATURES)

        return label_data


class DIETClassifierEntity(DIETClassifier):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
    
        ## FILTER START
        intent_filters = self.component_config['intent_filters']
        
        print(f'Filter intents : {intent_filters}')
        
        if intent_filters:
            backup_training_data_training_examples = training_data.training_examples
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in intent_filters]
            training_data.training_examples = filtered_training_examples

            print(f'    All example size : {len(backup_training_data_training_examples)}')
            print(f'    Filtered example size : {len(filtered_training_examples)}')
        ## FILTER END

        super().train(training_data, config, **kwargs)
        
        ## FILTER RECOVER START
        if intent_filters:
            training_data.training_examples = backup_training_data_training_examples

        ## FILTER RECOVER END

        
    def process(self, message: Message, **kwargs: Any) -> None:
        
        intent_filters = self.component_config['intent_filters']
        intent = message.get(INTENT)['name']

        # if intent == 'inform#history_tr- Flo giyim' and 'history_tr' in intent_filters:
        #     print('ENTERED')
        #     super().process(message, **kwargs)
        #     entities = message.get(ENTITIES, [])
        #     print(entities)

        if intent in intent_filters:
            super().process(message, **kwargs)

        ## TODO: REMOVE
        # super().process(message, **kwargs)
        # entities = message.get(ENTITIES, [])
        # message.set('_'.join(intent_filters), entities, add_to_output=True)
        # message.set(ENTITIES, [])
        pass

class DIETClassifier20201220(DIETClassifier):
    
    def batch_process(self, training_data):

        prediction_batch_size = self.component_config['prediction_batch_size'] if 'prediction_batch_size' in self.component_config else 256
        print(f'  Number of batches to be executed : {len(training_data.training_examples)//prediction_batch_size +1}')
        
        for i in range(len(training_data.training_examples)//prediction_batch_size +1):
            if i == len(training_data.training_examples)//prediction_batch_size:
                print(f'  Last batch. Batch idx : {i}')
            elif i % 20 == 0:
                print(f'  Batch idx : {i}')

            batch_data = training_data.training_examples[ i*prediction_batch_size: (i+1)*prediction_batch_size ]
            model_data = self._create_model_data(batch_data, training=False)
            batch_in = model_data.prepare_batch()
            out = self.model.batch_predict(batch_in)

            for k in out:
                out[k] = out[k].numpy()

            for j, message in enumerate(batch_data):                
                if self.component_config["prediction_condition"] is not False:
                    condition_attribute, condition_value = self.component_config["prediction_condition"]
                    predicted_value = message.get(condition_attribute)
                    predicted_value = predicted_value['name'] if ['name'] in predicted_value else predicted_value
                    if condition_value != predicted_value:
                        continue

                ## TODO need to be updated
                if self.component_config["intent_classification"]:
                    intent = message.get(INTENT)
                    if self.component_config["prediction_intent_write_attribute"] is not False:
                        message.set(self.component_config["prediction_intent_write_attribute"], intent, )
            
                
                if self.component_config["entity_recognition"]:
                    
                    predict_out = {k:tf.constant([out[k][j,:]]) for k in out}
                    predicted_tags = self._entity_label_to_tags(predict_out)
                    entities = self.convert_predictions_into_entities(message.text, message.get(TOKENS_NAMES[TEXT], []), predicted_tags)
                    entities = self.add_extractor_name(entities)

                    if self.component_config["prediction_entity_write_attribute"] is not False:
                        message.set(self.component_config["prediction_entity_write_attribute"], entities, )
    

    def train(self,training_data: TrainingData,config: Optional[RasaNLUModelConfig] = None,**kwargs: Any,) -> None:
    
        super().train(training_data, config, **kwargs)
        
        if self.component_config["prediction_in_train_time"]:
            # self.process(message,) single processing
            self.batch_process(training_data)
    
    def process(self, message: Message, **kwargs: Any) -> None:
        
        ## prediction condition
        if self.component_config["prediction_condition"] is not False:
            condition_attribute, condition_value = self.component_config["prediction_condition"]
            predicted_value = message.get(condition_attribute)
            predicted_value = predicted_value['name'] if ['name'] in predicted_value else predicted_value
            if condition_value != predicted_value:
                return None

        ## prediction
        super().process(message, **kwargs)
        
        if self.component_config["intent_classification"]:
            intent = message.get(INTENT)
            if self.component_config["prediction_intent_write_attribute"] is not False:
                message.set(self.component_config["prediction_intent_write_attribute"], intent, add_to_output=True )
    
        if self.component_config["entity_recognition"]:
            entities = message.get(ENTITIES, [])
            entities = [e for e in entities if e['extractor'] in 'DIETClassifier20201220' ]     
            if self.component_config["prediction_entity_write_attribute"] is not False:
                message.set(self.component_config["prediction_entity_write_attribute"], entities, add_to_output=True)
    

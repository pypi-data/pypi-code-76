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
import numpy as np
import scipy.sparse

try:
    import stanza
except:
    import_stanza = False

# %%

class LMTokenizer(Tokenizer, SparseFeaturizer):

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:

        super().__init__(component_config)

        self.nlp = stanza.Pipeline('tr')


    def _apply_lm(self, message: Message, attribute: Text) -> None:
        text = message.get(attribute)
        text = xNormalizer.clean_text(text)

        if text[-1] not in "?!.":
            text += " ."

        doc = self.nlp(text)  
    
        return doc

    def _get_lm_tokens(self, doc:Any) -> Any:
        tokens = doc.to_dict()
        tokens = [item for sublist in tokens for item in sublist]

        temp = []
        for item in tokens:
            try:
                int(item['id'])
                temp.append(item)
            except:
                pass
        tokens = temp
        return tokens

    def _lm_featurize(self, doc:Any, attribute:Any, ) -> Any:

        """
        def expand_feats(feats):

            if 'feats' in feats:
                feats = feats['feats']
                feats = {k:v for feat in feats.split('|') for (k,v) in (tuple(feat.split('=')),) }
            else:
                feats = {}
                
            feats = [feats['Case'] if 'Case' in feats else none_value, 
                    feats['Number'] if 'Number' in feats else none_value, 
                    feats['Person'] if 'Person' in feats else none_value,] 
            return feats
        """
        ##################################################################################
        # xpos, <date> <email> <url> <amount-of-money> <iban> <card-number> <city> 
        # <kredi karti> <kredi_kartindan>
        # 
        # 
        # <num> >> <ddd> <ddddd> <dd.dd>
        lm_features = {
            'upos' : ['NOUN', 'PROPN', 'ADJ', 'ADP', 'ADV', 'NUM', 'VERB', 'PUNCT', 'AUX', ],
            'deprel' : ['root', 'punct', 'nmod:poss', 'obj', 'nsubj', 'nmod', 'case', 'compound', 'nummod', 'flat', 'amod', 'conj', ],
            'feats' : ['Case=Nom', 'Case=Abl', 'Case=Dat', 'Case=Loc', 'Case=Acc'],
        }
        ##################################################################################

        lm_tokens = self._get_lm_tokens(doc)
        seq_length = len(lm_tokens) + 1
        feature_length = sum([len(v) for v in lm_features.values() ])
        vec = np.zeros([seq_length, feature_length])

        running_offset = 0

        for feature_key in lm_features:
            patterns = lm_features[feature_key]

            for pattern_index, pattern in enumerate(patterns):
                
                for token_index, t in enumerate(lm_tokens):

                    if feature_key not in t:
                        continue

                    if pattern == t[feature_key] or pattern in t[feature_key].split('|'):
                        vec[token_index][running_offset + pattern_index] = 1.0

                        if attribute in [RESPONSE, TEXT]:
                            # CLS token vector should contain all patterns
                            vec[-1][running_offset + pattern_index] = 1.0
                            
            running_offset += len(patterns)
        return scipy.sparse.coo_matrix(vec)

    def _set_lm_features(self, message:Any, doc:Any, attribute:Any, ) -> Any:

        features = self._lm_featurize(doc, attribute)
        features = SparseFeaturizer._combine_with_existing_sparse_features(message, features, feature_name=SPARSE_FEATURE_NAMES[attribute])
        message.set(SPARSE_FEATURE_NAMES[attribute], features)

    def align_entities(self, entities, tokens):

        aligned_entities = []
        
        e_len = len(entities)
        t_len = len(tokens)
        
        e_idx = 0
        t_idx = 0
        t_running_offset = 0
        t_running_offset_v2 = 0
        
        while True:
            
            e_matched_bool = False
            e_value = entities[e_idx]['value']
            e_running_offset = entities[e_idx]['start']
            e_end_offset = entities[e_idx]['end']
            
            t_value = tokens[t_idx]['text']
            t_end_offset = t_running_offset + len(t_value)
            t_end_offset_v2 = t_running_offset_v2 + len(t_value)
            
            ##########################################
            
            value_bool = t_value in e_value 
            start_bool = t_running_offset_v2 == e_running_offset
            end_bool = t_end_offset_v2 == e_end_offset
            
            match_ratio = max(min(t_end_offset_v2, e_end_offset) - max(t_running_offset_v2, e_running_offset), 0) / min(t_end_offset_v2 - t_running_offset_v2, e_end_offset - e_running_offset)
            
            ##########################################
            
            if start_bool or end_bool or match_ratio > 0.1:
                
                if 'role' in entities[e_idx]:
                    aligned_entities.append({
                        'value': t_value,
                        'entity': entities[e_idx]['entity'],
                        'role': entities[e_idx]['role'],
                        'start': t_running_offset,
                        'end': t_end_offset,
                    })
                else:
                    aligned_entities.append({
                        'value': t_value,
                        'entity': entities[e_idx]['entity'],
                        'start': t_running_offset,
                        'end': t_end_offset,
                    })
            
                if e_end_offset <= t_end_offset_v2:
                    e_idx += 1
            
            ##########################################
            
            # print(start_bool, end_bool, match_ratio)
            # print(e_value, t_value, )
            # print('e',e_running_offset, 'tv2',t_running_offset_v2)
            
            ##########################################
            
            if e_idx == e_len:
                break
            
            ##########################################
            
            t_idx += 1
            t_running_offset = t_end_offset + 1
            t_running_offset_v2 = min(  t_end_offset_v2 + 1,  
                                        max(aligned_entities[-1]['end'] 
                                                if aligned_entities else 0, 
                                            entities[e_idx]['start']
                                        )  
                                    )
            
            ##########################################
            
            if t_idx == t_len:
                print()
                print(" PROBLEM - NOT ALL ENTITIES ARE MATCHED ")
                
                print('entities', '\n', entities, '\n')
                print('tokens', '\n', tokens, '\n')
                break
                

        return aligned_entities

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Tokenize all training data."""

       
        for message in training_data.training_examples:
            for attribute in MESSAGE_ATTRIBUTES:
                if message.get(attribute) is not None:
                    if attribute == INTENT:
                        tokens = self._split_intent(message)
                        message.set(TOKENS_NAMES[attribute], tokens) # same line exist in else for TEXT and RESPONSE
                    else:
                        doc = self._apply_lm(message, attribute)
                        lm_tokens = self._get_lm_tokens(doc)
                        words = [token['text'] for token in lm_tokens]
                        text = " ".join(words)

                        if attribute == TEXT:
                            message.set(attribute, text) # update text # NOT WORKING # will be fixed with package after 18.05
                            message.text = text # WORKING
                        elif attribute == RESPONSE:
                            message.set(attribute, text)
                        
                        tokens = Tokenizer._convert_words_to_tokens(words, text)
                        tokens = Tokenizer.add_cls_token(tokens, attribute)
                        message.set(TOKENS_NAMES[attribute], tokens)

                        ## SET SPARSE LM FEATURES
                        if attribute == TEXT:
                            self._set_lm_features(message, doc, attribute, )

                        ## ALIGN ENTITIES
                        if attribute == TEXT:
                            
                            entities = message.get(ENTITIES)
                            if entities:
                                lm_tokens = self._get_lm_tokens(doc)
                                updated_entities = self.align_entities(entities, lm_tokens)
                                message.set(ENTITIES, updated_entities)


    def process(self, message: Message, **kwargs: Any) -> None:
        """Tokenize the incoming message."""

        doc = self._apply_lm(message, TEXT)
        lm_tokens = self._get_lm_tokens(doc)
        words = [token['text'] for token in lm_tokens]
        text = " ".join(words)
        
        message.set(TEXT, text) # update text # NOT WORKING # will be fixed with package after 18.05      
        message.text = text
        
        tokens = Tokenizer._convert_words_to_tokens(words, text)
        tokens = Tokenizer.add_cls_token(tokens, TEXT)
        message.set(TOKENS_NAMES[TEXT], tokens)

        self._set_lm_features(message, doc, TEXT, )

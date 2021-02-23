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
from rasa.nlu.extractors.extractor import EntityExtractor
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
from rasa.nlu.constants import TEXT, SPACY_DOCS, DENSE_FEATURIZABLE_ATTRIBUTES

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

#####################################################

try:
    import stanza
except:
    import_stanza = False
import spacy

from spacy.lang.tr import Turkish as SpacyTurkish
from pyspace.nlp.toolkit.spacy import SpacyMatcherMerger, SpacyStanzaPipeline
from pyspace.nlp.toolkit.spacy import SpacyPostTokenizer, SpacyTokenizer, SpacyRegexReplaceNormalizer, SpacyWhitespaceNormalizer, SpacyEndPunctuationNormalizer

from spacymoji import Emoji

from pyspace.nlp.toolkit.spacy import SpacyNLP

######################################################

from pyspace.nlp.dataset.alignment import align_fuzzy_multi
try:
    from jellyfish import jaro_similarity 
except:
    pass
#####################################################


# %%

class RasaSpacyTokenizer(Tokenizer, SparseFeaturizer, EntityExtractor):

    
    defaults = {
        
        'embedding_model': False,
        
        "whitespace_normalizer": True,
        "predefined_token_patterns":False, 
        "predefined_replace_patterns":False,
        
        "post_tokenization_bool":True,
        "post_tokenization_merge_bool":True, 
            
        "emoji_bool":True,
        "stanza_bool":True,

        "predefined_matcher_bool": False,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:

        super().__init__(component_config)
        
        self.embedding_model = self.component_config["embedding_model"]
        self.whitespace_normalizer = self.component_config["whitespace_normalizer"]
        self.predefined_token_patterns = self.component_config["predefined_token_patterns"]
        self.predefined_replace_patterns = self.component_config["predefined_replace_patterns"]

        self.post_tokenization_bool = self.component_config["post_tokenization_bool"]
        self.post_tokenization_merge_bool = self.component_config["post_tokenization_merge_bool"]
        
        self.emoji_bool = self.component_config["emoji_bool"]
        self.stanza_bool = self.component_config["stanza_bool"]
        self.predefined_matcher_bool = self.component_config["predefined_matcher_bool"]

        matchers = [
            ('<roomcount>', [[{"TEXT": {"REGEX": r"^(\d\+\d|10\+1)$"}}]]), # match one token '4+1'
            ('<amount-of-money>', [
                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(\$|tl|lira)$"}}], # match two tokens '100', '$'
                [{"LOWER": {"REGEX": r"^\d+(\.\d+)*(\$|tl|lira)$"}},], # match two tokens '100$'
            ]),
            ('<totalfloorcount>', [
                [{"TEXT": {"REGEX": r"^\d+$"}}, {"LOWER": {"REGEX": r"^katl[i|ı]$"}}],
            ]),
            ('<currentfloorcount>', [
                [{"TEXT": {"REGEX": r"^\d+$"}}, {"LOWER": {"REGEX": r"^(\.|inci|ıncı)$"}}, {"LOWER": {"REGEX": r"^kat(ta)*$"}}],
                [{"LOWER": {"REGEX": r"^\d+(\.|inci|ıncı|nci|ncı)$"}}, {"LOWER": {"REGEX": r"^kat(|ta)$"}}],
                [{"LOWER": {"REGEX": r"^(ara|bodrum)$"}}, {"LOWER": {"REGEX": r"^kat(|ta)$"}}],
                [{"LOWER": {"REGEX": r"y[u|ü]ksek"}}, {"LOWER": {"REGEX": r"giri[s|ş]"}}],
                
            ]),
            ('<squaremeter>', [
                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"TEXT": {"REGEX": r"^[\+\-]$"}}, {"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metre)$"}}, {"LOWER": {"REGEX": r"^(kare)$"}}],
                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"TEXT": {"REGEX": r"^[\+\-]$"}}, {"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metrekare(lik|den)*|m2)$"}}],

                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"TEXT": {"REGEX": r"^[\+\-]\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metre)$"}}, {"LOWER": {"REGEX": r"^(kare)$"}}],
                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"TEXT": {"REGEX": r"^[\+\-]\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metrekare(lik|den)*|m2)$"}}],

                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metre)$"}}, {"LOWER": {"REGEX": r"^(kare)$"}}],
                [{"TEXT": {"REGEX": r"^\d+(\.\d+)*$"}}, {"LOWER": {"REGEX": r"^(metrekare(lik|den)*|m2)$"}}],
                [{"LOWER": {"REGEX": r"^\d+(\.\d+)*(m2)$"}}, ],
            ]),
            ('<yearsold>', [
                [{"TEXT": {"REGEX": r"^\d+$"}}, {"LOWER": {"REGEX": r"^(yıl)"}}, ],
            ]),
            ('<housefacing>', [
                [{"LOWER": {"REGEX": r"^(on|ön|arka|guney|güney|cift|çift|genis|geniş)$"}}, {"LOWER": {"REGEX": r"^cephe.*?$"}}, ],
            ]),

            ('<date>', [
                [{"TEXT": {"REGEX": r"^\d\d(\/|-|\.)\d\d(\/|-|\.)\d\d\d\d$"}}, ],
                [{"TEXT": {"REGEX": r"^\d\d\d\d(\/|-|\.)\d\d(\/|-|\.)\d\d$"}}, ],
            ]),
            ('<url>', [
                [{"LIKE_URL": True}, ],
            ]),
            ('<email>', [
                [{"LIKE_EMAIL": True}, ],
            ]),
            
            
            ('<USA>'      , [[{"TEXT": {"REGEX": "^[Uu](\.?|nited)$"}}, {"TEXT": {"REGEX": "^[Ss](\.?|tates)$"}}]]), # match two tokens 'United', 'States'
                    ]
        # matchers = []

        ############################################
        ############################################
        ############################################

        # phrasematcher # # match merge and label
        # phrasematchers = [('specialroom', ['a3+1'])]
        phrasematchers = [('<loc>',['e-5', ])]

        ############################################
        ############################################
        ############################################

        # token match # # merge / split token match
        token_patterns = [
            r'\b\d\+\d\b', # match '1+1'
            r'\b10\+1\b', # exact match '10+1'
            r'\d+(\.\d+)*\s*(\$|tl|lira)', # match '1000$'
                        ]
        # token_patterns = []

        ############################################
        ############################################
        ############################################

        # normalze text # # replace with regex  
        replace_patterns = [
            (r'\b(\d)\s*(\+)\s*([\d])\b', r'\1\2\3'), # replace '2 + 1' to '2+1'
            (r'\b(\d+(\.\d+)*(\$|tl|lira))(\S+?)(\s)', r'\1 \4 '), # replace '100$. ' to '100$ . '
            (r'(?<![\d\.])([^\s\d])(\d+(\.\d+)*(\s)(\$|tl|lira))(\s)', r'\1 \2\4'), # replace '-100$' to '- 100$ '
                            ]
        # replace_patterns = []

        ############################################
        ############################################
        ############################################

        config = {
            'embedding_model':self.embedding_model,
            'whitespace_normalizer':self.whitespace_normalizer,
            'token_patterns':token_patterns if self.predefined_token_patterns else [], 
            'replace_patterns':replace_patterns if self.predefined_replace_patterns else [],
            
            'post_tokenization_bool':self.post_tokenization_bool,
            'post_tokenization_merge_bool':self.post_tokenization_merge_bool, 
            'emoji_bool':self.emoji_bool,
            'stanza_bool':self.stanza_bool,

            'matchers':matchers if self.predefined_matcher_bool else [],
            'phrasematchers':phrasematchers if self.predefined_matcher_bool else [],
        }
        nlp = SpacyNLP(config)

        if self.predefined_matcher_bool:            
            __dm = nlp.get_pipe(SpacyMatcherMerger.name).custom_defaultmatcher
            self.spacy_ents =  [r[0] for r in matchers] + [r[0] for r in phrasematchers] + [ __dm.vocab.strings[p] for p in list(__dm._patterns.keys())]
            self.spacy_ents =  [ v for (i,v) in enumerate(self.spacy_ents) if v not in self.spacy_ents[0:i] ]

        self.nlp = nlp

    def _spacy_featurize(self, doc:Any, attribute:Any, ) -> Any:

        # doc.ents

        # span = doc.ents[0]
        # span.label_

        # token = span[0]
        # token = doc[0] 
        # token.ent_type_

        # <roomcount>
        # <amount-of-money>
        # <totalfloorcount>

        spacy_features = {}
        
        if self.predefined_matcher_bool:
            spacy_features['ent_type_'] = self.spacy_ents
            
        if self.stanza_bool:
            spacy_features['pos_'] = ['NOUN', 'PROPN', 'ADJ', 'ADP', 'ADV', 'NUM', 'VERB', 'PUNCT', 'AUX', ]
            spacy_features['dep_'] = ['root', 'punct', 'nmod:poss', 'obj', 'nsubj', 'nmod', 'case', 'compound', 'nummod', 'flat', 'amod', 'conj', ]
            spacy_features['feats_'] = ['Case=Nom', 'Case=Abl', 'Case=Dat', 'Case=Loc', 'Case=Acc']
        

        
        seq_length = len(doc) + 1
        feature_length = sum([len(v) for v in spacy_features.values() ])

        if feature_length != 0:
            vec = np.zeros([seq_length, feature_length])

            running_offset = 0

            for feature_key in spacy_features:
                patterns = spacy_features[feature_key]

                for pattern_index, pattern in enumerate(patterns):
                    
                    for token_index, t in enumerate(doc):

                        if (False
                            or pattern == getattr(t, feature_key, False)
                            or pattern == getattr(t._, feature_key, False)
                            or pattern in getattr(t._, feature_key, '').split('|')
                        ):
                            vec[token_index][running_offset + pattern_index] = 1.0

                            if attribute in [RESPONSE, TEXT]:
                                # CLS token vector should contain all patterns
                                vec[-1][running_offset + pattern_index] = 1.0
                                
                running_offset += len(patterns)

            explain_features = False
            if explain_features:
                from tabulate import tabulate
                import pandas as pd
                df = pd.DataFrame(vec, 
                    columns = [f for k,v in spacy_features.items() for f in v],
                    index = [t.text for t in doc] + ['CLS']
                )
                print(tabulate(df,headers='keys',tablefmt='psql'))
                print()
                print()

            return scipy.sparse.coo_matrix(vec)
        else:
            return None

    def _set_spacy_features(self, message:Any, doc:Any, attribute:Any, ) -> Any:

        features = self._spacy_featurize(doc, attribute)
        if str(type(features)) != str(type(None)):
            features = SparseFeaturizer._combine_with_existing_sparse_features(message, features, feature_name=SPARSE_FEATURE_NAMES[attribute])
            message.set(SPARSE_FEATURE_NAMES[attribute], features)

    def _spacy_get_entities(self, message:Any, doc:Any, attribute:Any, ) -> Any:

        rasa_tokens = message.get(TOKENS_NAMES[attribute], [])
        feature_key = 'ent_type_'

        extracted = []
        for token_index, t in enumerate(doc):

            if '' != getattr(t, feature_key):
        
                entity = {
                    "start": rasa_tokens[token_index].start,
                    "end": rasa_tokens[token_index].end,
                    "value": rasa_tokens[token_index].text,
                    # "confidence": 1.0,
                    "entity": getattr(t, feature_key),
                }
                extracted.append(entity)
        extracted = self.add_extractor_name(extracted)
        return extracted

    def _set_spacy_entities(self, message:Any, doc:Any, attribute:Any, ) -> Any:
        extracted = self._spacy_get_entities(message, doc, attribute)
        message.set("entities", message.get("entities", []) + extracted, add_to_output=True)

    def _tokenize(self, message:Any, attribute:Any) -> Any:
        text = message.get(attribute)
        if attribute == TEXT:
            entities = message.get(ENTITIES)
            if entities:
                doc, entities = self.nlp(text, entities)
                message.set(ENTITIES, entities)
            else:
                doc = self.nlp(text,)
        else:
            doc = self.nlp(text,)

        words = [token.text for token in doc]
        text = doc.text
        message.set(attribute, text) # update text # NOT WORKING FOR TEXT # will be fixed with package after 18.05
        if attribute == TEXT:
            message.text = text # WORKING

        tokens = Tokenizer._convert_words_to_tokens(words, text)
        tokens = Tokenizer.add_cls_token(tokens, attribute)
        message.set(TOKENS_NAMES[attribute], tokens)

        if attribute == TEXT:
            self._set_spacy_features(message, doc, attribute, )
            message.set(SPACY_DOCS[attribute], doc)

        return doc

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
                        message.set(TOKENS_NAMES[attribute], tokens)

                    elif attribute in [RESPONSE, TEXT]:

                        doc = self._tokenize(message, attribute)

    def process(self, message: Message, **kwargs: Any) -> None:
        """Tokenize the incoming message."""

        doc = self._tokenize(message, TEXT)
        self._set_spacy_entities(message, doc, TEXT, )

        

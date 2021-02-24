import logging
import os
import re
from typing import Any, Dict, List, Optional, Text, Union, Type

import warnings
from rasa.nlu.utils import write_json_to_file

import numpy as np
import copy

from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
import rasa.utils.io
import rasa.utils.io
import scipy.sparse
from rasa.nlu import utils
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
)
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

import pyspace
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
from pyspace.nlp.dataset.load_data import load_branches, load_names, load_billing_agencies
from pyspace.re.refunctions import convert_list_to_regex

logger = logging.getLogger(__name__)


class RegexFeaturizerExtended(SparseFeaturizer):

    defaults = {
        "tr_normalize": True,
        "re_ignore_case": True,
    }

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        return [Tokenizer]

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        known_patterns: Optional[List[Dict[Text, Text]]] = None,
        lookup_tables: Optional[List[Dict[Text, Union[Text, List]]]] = None,
    ) -> None:

        super().__init__(component_config)

        self.tr_normalize = self.component_config["tr_normalize"]
        self.re_ignore_case = self.component_config["re_ignore_case"]
        

        self.known_patterns = known_patterns if known_patterns else []
        lookup_tables = lookup_tables or []
        self._add_lookup_table_regexes(lookup_tables)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        self.known_patterns = training_data.regex_features
        self._add_lookup_table_regexes(training_data.lookup_tables)

        for example in training_data.training_examples:
            for attribute in [TEXT, RESPONSE]:
                self._text_features_with_regex(example, attribute)

    def process(self, message: Message, **kwargs: Any) -> None:
        # print('regex featurizer process')
        self._text_features_with_regex(message, TEXT)

    def _text_features_with_regex(self, message: Message, attribute: Text) -> None:
        if self.known_patterns:
            extras = self._features_for_patterns(message, attribute)
            features = self._combine_with_existing_sparse_features(
                message, extras, feature_name=SPARSE_FEATURE_NAMES[attribute]
            )
            message.set(SPARSE_FEATURE_NAMES[attribute], features)

    def _add_lookup_table_regexes(
        self, lookup_tables: List[Dict[Text, Union[Text, List]]]
    ) -> None:
        """appends the regex features from the lookup tables to self.known_patterns"""
        for table in lookup_tables:
            regex_pattern = self._generate_lookup_regex(table)
            lookup_regex = {"name": table["name"], "pattern": regex_pattern}
            self.known_patterns.append(lookup_regex)

    def _features_for_patterns(
        self, message: Message, attribute: Text
    ) -> Optional[scipy.sparse.coo_matrix]:
        """Checks which known patterns match the message.
        Given a sentence, returns a vector of {1,0} values indicating which
        regexes did match. Furthermore, if the
        message is tokenized, the function will mark all tokens with a dict
        relating the name of the regex to whether it was matched."""

        # Attribute not set (e.g. response not present)
        if not message.get(attribute):
            return None

        tokens = message.get(TOKENS_NAMES[attribute], [])

        if not tokens:
            # nothing to featurize
            return

        seq_length = len(tokens)

        vec = np.zeros([seq_length, len(self.known_patterns)])

        for pattern_index, pattern in enumerate(self.known_patterns):

            __pattern = pattern["pattern"]
            __text = xNormalizer.tr_normalize(message.text).lower()
            __flag = re.I

            try:
                matches = re.finditer(__pattern, __text, __flag)
                matches = list(matches)
            except:
                
                print('regex featurizer extended process error')
                print(__pattern)

            for token_index, t in enumerate(tokens):
                patterns = t.get("pattern", default={})
                patterns[pattern["name"]] = False

                if t.text == CLS_TOKEN:
                    # make sure to set all patterns for the CLS token to False
                    # the attribute patterns is needed later on and in the tests
                    t.set("pattern", patterns)
                    continue

                for match in matches:
                    if t.start < match.end() and t.end > match.start():
                        patterns[pattern["name"]] = True
                        vec[token_index][pattern_index] = 1.0
                        if attribute in [RESPONSE, TEXT]:
                            # CLS token vector should contain all patterns
                            vec[-1][pattern_index] = 1.0

                t.set("pattern", patterns)


        
        #from tabulate import tabulate
        #import pandas as pd
        #df = pd.DataFrame(vec, 
        #    columns = [pattern['name'] for pattern_index, pattern in enumerate(self.known_patterns)],
        #    index = [t.text for t in tokens]
        #)
        #print(tabulate(df,headers='keys',tablefmt='psql'))
        #print()
        #print()
        return scipy.sparse.coo_matrix(vec)

    def _generate_lookup_regex(
        self, lookup_table: Dict[Text, Union[Text, List[Text]]]
    ) -> Text:
        """creates a regex out of the contents of a lookup table file"""
        lookup_elements = lookup_table["elements"]
        elements_to_regex = []

        # if it's a list, it should be the elements directly
        if isinstance(lookup_elements, list):
            elements_to_regex = lookup_elements
            common_utils.raise_warning(
                f"Directly including lookup tables as a list is deprecated since Rasa "
                f"1.6.",
                FutureWarning,
                docs=DOCS_URL_TRAINING_DATA_NLU + "#lookup-tables",
            )

        # otherwise it's a file path.
        else:

            try:
                f = open(lookup_elements, "r", encoding=rasa.utils.io.DEFAULT_ENCODING)
            except OSError:
                raise ValueError(
                    f"Could not load lookup table {lookup_elements}. "
                    f"Please make sure you've provided the correct path."
                )

            with f:
                for line in f:
                    new_element = line.strip()
                    if new_element:
                        elements_to_regex.append(new_element)

        # sanitize the regex, escape special characters
        elements_sanitized = [re.escape(e) for e in elements_to_regex]

        # regex matching elements with word boundaries on either side
        regex_string = "(?i)(\\b" + "\\b|\\b".join(elements_sanitized) + "\\b)"
        return regex_string

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["RegexFeaturizerExtended"] = None,
        **kwargs: Any,
    ) -> "RegexFeaturizerExtended":

        try:
            file_name = meta.get("file")
            regex_file = os.path.join(model_dir, file_name)

            if os.path.exists(regex_file):
                known_patterns = rasa.utils.io.read_json_file(regex_file)
                return RegexFeaturizerExtended(meta, known_patterns=known_patterns)
            else:
                return RegexFeaturizerExtended(meta)
        except:
            print('regex featurizer extended load error')

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory.
        Return the metadata necessary to load the model again."""
        file_name = file_name + ".pkl"
        regex_file = os.path.join(model_dir, file_name)
        utils.write_json_to_file(regex_file, self.known_patterns, indent=4)

        return {"file": file_name}



class RegexEntityExtractor(EntityExtractor):

    defaults = {
        "name_lookup_bool": True,
        "branch_lookup_bool": True,
        "billagency_lookup_bool": True,
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Text]] = None,
        regex_features: Optional[Dict[Text, Any]] = None
    ) -> None:
        super(RegexEntityExtractor, self).__init__(component_config)

        
        self.name_lookup_bool = self.component_config["name_lookup_bool"]
        self.branch_lookup_bool = self.component_config["branch_lookup_bool"]
        self.billagency_lookup_bool = self.component_config["billagency_lookup_bool"]

        self.regex_features = regex_features if regex_features else []

    def train(
        self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:

        additional_regex_features = []

        if self.billagency_lookup_bool:
            additional_regex_features.append({'name':'B-billing-agencies', 'group':2, 'pattern': load_billing_agencies(mode='list')})
        if self.name_lookup_bool:
            additional_regex_features.append({'name':'B-male-name'       , 'group':2, 'pattern': load_names(first_char_upper=True, mode='separate')[0]})
            additional_regex_features.append({'name':'B-female-name'     , 'group':2, 'pattern': load_names(first_char_upper=True, mode='separate')[1]})
            additional_regex_features.append({'name':'B-last-name'       , 'group':2, 'pattern': load_names(first_char_upper=True, mode='separate')[2]})
        if self.branch_lookup_bool:
            additional_regex_features.append({'name':'B-branch'          , 'group':2, 'pattern': load_branches(mode='list')})

        for item in additional_regex_features:
            item['pattern'] = convert_list_to_regex(item['pattern'])

        self.regex_features = copy.deepcopy(training_data.regex_features) + additional_regex_features
        

    def match_regex(self, message):
        extracted = []
        for d in self.regex_features:

            __pattern = d['pattern']
            __text = xNormalizer.tr_normalize(message).lower()
            __flag = re.I
            __group = 0 if 'group' not in d else d['group']

            try:
                # match = re.search(pattern=d['pattern'], string=message)
                matches = re.finditer(pattern=__pattern, string=__text, flags=__flag)
                matches = list(matches)
            except:
                print('regex entity extractor process error')
                print(__pattern)

            for match in matches:
                # match # whole token with word boundaries
                entity = {
                    "start": match.span()[0], # whole token start 
                    "end": match.span()[1], # whole token end
                    "value": match.group(__group), # regex entity group # e.g. without suffixes
                    # "confidence": 1.0,
                    "entity": d['name'],
                }
                extracted.append(entity)

        extracted = self.add_extractor_name(extracted)
        return extracted

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""
        # print('regex entity extractor process')

        extracted = self.match_regex(message.text)
        message.set("entities", message.get("entities", []) + extracted, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        import pickle
        regex_file_name = file_name + "_regex.pkl"
        with open(os.path.join(model_dir, regex_file_name), 'wb') as f:
            pickle.dump(self.regex_features, f)

        return {"regex_file_name": regex_file_name}

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional[Metadata] = None,
            cached_component: Optional["RegexEntityExtractor"] = None,
            **kwargs: Any
    ) -> "RegexEntityExtractor":

        # try except
        try:
            regex_file_name = meta.get("regex_file_name")
            regex_file = os.path.join(model_dir, regex_file_name)
            import pickle
            with open(regex_file, 'rb') as f:
                regex_features = pickle.load(f)

            # print(regex_features[-1])
        except:
            print('regex entity extractor load error')
        return cls(meta, regex_features)


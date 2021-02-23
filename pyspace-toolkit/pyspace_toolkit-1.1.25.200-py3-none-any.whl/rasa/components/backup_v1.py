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
from rasa.nlu.training_data import Message
from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES

# %%
from pyspace.nlp.toolkit.zemberek import lemmatize as zflemmatizer
from pyspace.nlp.toolkit.zemberek import tokenize as zftokenizer
from pyspace.nlp.toolkit.zemberek import normalize as zfnormalizer

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

# %%


import numpy as np

from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
import rasa.utils.io
import rasa.utils.io
import rasa.utils.io as io_utils
import scipy.sparse
from rasa.nlu import utils
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

from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata


import stanza
from sklearn.preprocessing import OneHotEncoder

# %%

class CustomFeaturizer(Tokenizer, SparseFeaturizer):

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:

        super().__init__(component_config)

        self.nlp = stanza.Pipeline('tr')


    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:

        for example in training_data.training_examples:
            for attribute in [TEXT, RESPONSE]:
                self._text_features_with_regex(example, attribute)

    def process(self, message: Message, **kwargs: Any) -> None:
        self._text_features_with_regex(message, TEXT)

    def _apply_lm(self, message: Message, attribute: Text) -> None:

        doc = nlp(text)        

    def _text_features_with_regex(self, message: Message, attribute: Text) -> None:
        if self.known_patterns:
            extras = self._features_for_patterns(message, attribute)
            features = self._combine_with_existing_sparse_features(
                message, extras, feature_name=SPARSE_FEATURE_NAMES[attribute]
            )
            message.set(SPARSE_FEATURE_NAMES[attribute], features)

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
            matches = re.finditer(pattern["pattern"], message.text)
            matches = list(matches)

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

        return scipy.sparse.coo_matrix(vec)

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional[Metadata] = None,
        cached_component: Optional["RegexFeaturizer"] = None,
        **kwargs: Any,
    ) -> "RegexFeaturizer":

        file_name = meta.get("file")
        regex_file = os.path.join(model_dir, file_name)

        if os.path.exists(regex_file):
            known_patterns = rasa.utils.io.read_json_file(regex_file)
            return RegexFeaturizer(meta, known_patterns=known_patterns)
        else:
            return RegexFeaturizer(meta)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this model into the passed directory.
        Return the metadata necessary to load the model again."""
        file_name = file_name + ".pkl"
        regex_file = os.path.join(model_dir, file_name)
        utils.write_json_to_file(regex_file, self.known_patterns, indent=4)

        return {"file": file_name}
# %%
class ZemberekTokenizer(Tokenizer):
    
    defaults = {
        "normalize": True,
        "lemmatize": True,
        "lowercase": True,
    }

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)

        self.normalize = self.component_config["normalize"]
        self.lemmatize = self.component_config["lemmatize"]
        self.lowercase = self.component_config["lowercase"]

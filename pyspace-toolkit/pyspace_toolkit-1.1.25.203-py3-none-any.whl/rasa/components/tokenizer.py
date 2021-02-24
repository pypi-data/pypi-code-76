# %%
# %% [markdown]
# https://rasa.com/docs/rasa/api/custom-nlu-components/
# If you create a custom tokenizer you should implement the methods of rasa.nlu.tokenizers.tokenizer.Tokenizer. The train and process methods are already implemented and you simply need to overwrite the tokenize method. train and process will automatically add a special token __CLS__ to the end of list of tokens, which is needed further down the pipeline.

# %%
import re
from typing import Any, Dict, List, Text

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
class CustomTokenizer(Tokenizer):
    
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""

        super().__init__(component_config)
        self.case_sensitive = self.component_config["case_sensitive"]

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)

        if not self.case_sensitive:
            text = text.lower()

        # remove 'not a word character' if
        words = re.sub(
            # there is a space or an end of a string after it
            r"[^\w#@&]+(?=\s|$)|"
            # there is a space or beginning of a string before it
            # not followed by a number
            r"(\s|^)[^\w#@&]+(?=[^0-9\s])|"
            # not in between numbers and not . or @ or & or - or #
            # e.g. 10'000.00 or blabla@gmail.com
            # and not url characters
            r"(?<=[^0-9\s])[^\w._~:/?#\[\]()@!$&*+,;=-]+(?=[^0-9\s])",
            " ",
            text,
        ).split()
        # if we removed everything like smiles `:)`, use the whole text as 1 token
        if not words:
            words = [text]

        return self._convert_words_to_tokens(words, text)


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

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)

        text = xNormalizer.clean_text(text)
        
        if self.normalize:
            text = zfnormalizer(text)
        
        if not self.lemmatize and self.lowercase:
            text = text.lower()
        
        words = zftokenizer(text, mode=1)
        
        
        
        if self.lemmatize:
            words = [zflemmatizer(word) for word in words]

        text = " ".join(words)
        
        return self._convert_words_to_tokens(words, text)

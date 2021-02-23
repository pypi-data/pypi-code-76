
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
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

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
# from pyspace.nlp.toolkit.zemberek import normalize, lemmatize

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

import re
import string

class PyspaceNormalizer(Component):

    def normalize_tokens(self, tokens):
        # [self.normalize_token(t) for t in tokens]
        return False
    def normalize_text(self, text):
        return False

    def normalize_message(self, message):

        if self.normalize_tokens(["message"]) != False:
            
            tokens = [t.text for t in message.data["tokens"] if t.text != '__CLS__']

            ###########################################################################
            
            tokens = self.normalize_tokens(tokens) 

            ###########################################################################

            if self.normalize_text("message") != False:
                norm = self.normalize_text(message.text.replace('__CLS__','').strip())
            else:
                norm = " ".join(tokens)
            message.text = norm
            message.set(TEXT, norm)
            
            tokens = Tokenizer._convert_words_to_tokens(tokens, norm)
            tokens = Tokenizer.add_cls_token(tokens, TEXT)
            message.set(TOKENS_NAMES[TEXT], tokens)
            
        elif self.normalize_text("message") != False:

            norm = self.normalize_text(message.text)

            message.text = norm
            message.set(TEXT, norm)


    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.normalize_message(message)

    def process(self, message: Message, **kwargs: Any):

        self.normalize_message(message)

##########################################################################################3
##########################################################################################3

class ZemberekNormalizer(PyspaceNormalizer):

    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import normalize
        self.normalize = normalize
        super().__init__(component_config)
    
    def normalize_text(self, text):
        return self.normalize(text)


class ZemberekLemmatizer(PyspaceNormalizer):

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import lemmatize
        self.lemmatize = lemmatize
        super().__init__(component_config)
        
    def normalize_tokens(self, tokens):
        return [self.lemmatize(t) for t in tokens]

class TurkishCharacterNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        return [xNormalizer.tr_normalize(t) for t in tokens]

    def normalize_text(self, text):
        return xNormalizer.tr_normalize(text)

class PunctuationNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        
        output = []
        for t in tokens: 
            temp = re.sub(fr"""[{re.escape(string.punctuation)}]""", '', t).strip()
            if temp != '':
                output.append(temp)
        return output


class LowercaseNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "EN",
    }

    def normalize_tokens(self, tokens):
        return [xNormalizer.lower(t, lang=self.component_config["lang"]) for t in tokens]
    
    def normalize_text(self, text):
        return xNormalizer.lower(text, lang=self.component_config["lang"])

class StopwordsNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "TR",
    }
    

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        # TODO
        # from pyspace_resources.stopwords.turkish import stopwords
        self.stopwords = self.component_config["stopwords"]

    def normalize_tokens(self, tokens):

        return [t for t in tokens if t not in self.stopwords]
    


##########################################################################################3
##########################################################################################3
class EntityNormalization(Component):

    defaults = {
        'normalization_config' : [
            ['entities', 'DIETClassifier', 'B-AMOUNT-OF-MONEY', '', 'A'],
        ],
    }

    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, ):

        # assert message.data["tokens"] == message.get(TOKENS_NAMES[TEXT])
        tokens = message.get(TOKENS_NAMES[TEXT])

        for n in self.component_config["normalization_config"]:
            attr, classifier_name, entity_name, role, replacement = n

            entities = message.get(attr)
            # entities = [e for e in entities if e['extractor'] in [classifier_name] and e['entity'] in [entity_name] ]
            entities = [e for e in entities if e['extractor'] in [classifier_name] and e['entity'] in [entity_name] and role in [e.get("role", "")] ]
            entities = sorted(entities, key=lambda e:e['start'])

            result = []
            e_end = -1
            for token in tokens:
                # token['normalized'] = True
                if e_end >= token.end:
                    continue  
                for e in entities:
                    startbool = token.start >= e['start']
                    endbool = token.end <= e['end']

                    if startbool and endbool:
                        token.text = replacement
                        token.lemma = token.text
                        token.end = e['end']
                result.append(token)
                e_end = token.end
            tokens = result
            # for token in tokens:
            #     for e in entities:
            #         startbool = token.start >= e['start']
            #         endbool = token.end <= e['end']
            #         if startbool and endbool:
            #             token.text = replacement
            #             token.lemma = token.text

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.normalize(message,)            

    def process(self, message: Message, **kwargs: Any):
        self.normalize(message,)


class EntityNormalizationBackup(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    
                    
                    if self.print_example_count != 0:

                        if token.text not in e['value']:
                            print('Token text is not in entity value.')

                            self.print_example_count -= 1

                            print(message.text)
                            print(token.text, token.start, token.end)
                            print(e)
                            print(entities)
                            print()

                    # assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    token.lemma = token.text
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        print('  train function')
        self.print_example_count = 5

        for message in training_data.training_examples:
            entities = message.get('norm_ent')
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        print('  process function')
        self.print_example_count = 0
        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        self.normalize(message, entities)


class DucklingEntityNormalizationBackup(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(DucklingEntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    
                    
                    if self.print_example_count != 0:

                        if token.text not in e['value']:
                            print('Token text is not in entity value.')

                            self.print_example_count -= 1

                            print(message.text)
                            print(token.text, token.start, token.end)
                            print(e)
                            print(entities)
                            print()

                    # assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    token.lemma = token.text
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        print('  train function')
        self.print_example_count = 5

        for message in training_data.training_examples:
            entities = message.get(ENTITIES, [])
            entities = [e for e in entities if e['extractor'] in ['DucklingHTTPExtractor', 'DucklingExtractor', 'DucklingExtractorExtended']]
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        print('  process function')
        self.print_example_count = 0
        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DucklingHTTPExtractor', 'DucklingExtractor', 'DucklingExtractorExtended']]
        self.normalize(message, entities)

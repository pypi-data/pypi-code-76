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

from pyspace.nlp.task.date_extractor import DateParser

# %%
import copy
import pickle

import numpy as np
import scipy.sparse

import pytz
import datetime

try:
    import stanza
except:
    import_stanza = False
# %%

class TrainingDatasetPrediction(Component):

    def __init__(self, component_config: Dict[Text, Any] = None, t_dict=None) -> None:
        super(TrainingDatasetPrediction, self).__init__(component_config)
        self.t_dict = t_dict

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        self.t_dict = {}

        for message in training_data.training_examples:
            if message.text in self.t_dict and str(self.t_dict[message.text]) != str(message.get(INTENT)):
                print(message.text)
                print('  > ' + str(self.t_dict[message.text])  )
                print('  > ' + str(message.get(INTENT))  ) 
                print()
            self.t_dict[message.text] = message.get(INTENT)

    def process(self, message: Message, **kwargs: Any) -> None:

        if message.text in self.t_dict:
            message.set(INTENT, {'name': self.t_dict[message.text], 'confidence': 0.998})
    
    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        t_dict_file_name = file_name + "_t_dict.pkl"
        with open(os.path.join(model_dir, t_dict_file_name), 'wb') as f:
            pickle.dump(self.t_dict, f)
        return {"t_dict": t_dict_file_name, }

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir: Optional[Text] = None, model_metadata: Optional["Metadata"] = None, cached_component: Optional["Component"] = None, **kwargs: Any,) -> "Component":
        t_dict_file = os.path.join(model_dir, meta.get("t_dict"))
        with open(t_dict_file, 'rb') as f:
            t_dict = pickle.load(f)
        return cls(meta, t_dict,)

class MergeSubclasses(Component):
    defaults = {
        'subclass_delimiter': '___',
    }
    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        for message in training_data.training_examples:
            self.process(message)

    def process(self, message: Message, **kwargs: Any) -> None:
        dl = self.component_config['subclass_delimiter']
        intent = message.get(INTENT)

        # print(intent)
        # print(isinstance(intent, str))
        # print(type(intent))

        if isinstance(intent, dict):
            if dl in intent['name']:
                message.set(INTENT, {'name': intent['name'].rsplit(dl, 1)[0], 'confidence': intent['confidence']})

        elif isinstance(intent, str):
            if dl in intent:
                message.set(INTENT, intent.rsplit(dl, 1)[0])

    

class EntityManager(Component):

    defaults = {
        "priority_config": {},
        "merge_BI_entities": True,
        "merge_same_entities": False,
        "split_same_entities": False,
    }

    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityManager, self).__init__(component_config)
        
        self.priority_config = self.component_config["priority_config"]
        self.priority_config = { float(k):v for k,v in self.priority_config.items()}
        self.priority_config = [self.priority_config[i].split('___',1) for i in sorted (self.priority_config.keys())]

        # print()
        # print('Entity Priority List')
        # print(self.priority_config)
        # print()
        pass

    @staticmethod
    def base_func_to_merge_entity_subset_without_condition(entities):

        if len(entities) == 1:
            return entities
        else:
            entities_copy = copy.deepcopy(entities)

            temp_value = ""
            prev_index = entities[0]['start']
            for e in entities:
                temp_value += " "*(e['start'] - prev_index) + e['value']
                prev_index = e['end']
            
            entities[0]['value'] = temp_value
            entities[0]['end'] = entities[-1]['end']
            entities[0]['raw'] = entities_copy

            return [entities[0]]

    @staticmethod
    def base_func_to_merge_entity_subset(message, entities, ):
        temp = entities

        if len(temp) == 1:
            return temp
            
        else:
            if all([ temp[i+1]['start'] - temp[i]['end'] <= 1 for i in range(len(temp)-1)]):
                temp_value = message.text[temp[0]['start']:temp[-1]['end']]
                temp_value_norm = xNormalizer.tr_normalize(temp_value).lower()
                
                if all( [xNormalizer.tr_normalize(tt['value']).lower() in temp_value_norm for tt in temp]):
                    temp_copy = copy.deepcopy(temp)

                    temp[0]['value'] = temp_value
                    temp[0]['end'] = temp[-1]['end']
                    temp[0]['raw'] = temp_copy

                    return [temp[0]]
                else:
                    print()
                    print('Model entities are consecutive but not match with message. They are not merged.')
                    print(temp_value)
                    # print(model_entities)
                    print(temp)
                    return temp

            else:
                print()
                print('Model entities are not consecutive. They are not merged.')
                # print(model_entities)
                print(temp)
                return temp

    @staticmethod
    def split_one_entity(e):
        result = []
        
        temp_spaces = []
        for match in re.finditer(r"\s+", e['value']):
            temp_spaces.append(match.end() - match.start())
        temp_spaces += [0]

        start_index = e['start']
        for value_i, space_i in zip( re.split('\s+', e['value']), temp_spaces ):
            e_i = copy.deepcopy(e)
            e_i['start'] = start_index
            e_i['end'] = start_index + len(value_i)
            e_i['value'] = value_i
            start_index = start_index + len(value_i) + space_i

            result.append(e_i)

        return result

    @staticmethod
    def split_rasa_entity_merge(entities):
        entities_updated = entities

        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        splitted_model_entities = []
        for e in model_entities:
            if ' ' not in e['value']:
                splitted_model_entities.append(e)

            else:
                if e['entity'][:2] == 'B-':
                    splitted_model_entities.extend(EntityManager.split_one_entity(e))

                elif e['entity'][:2] == 'I-':
                    splitted_model_entities.append(e)

                else:
                    splitted_model_entities.extend(EntityManager.split_one_entity(e))


            entities_updated = splitted_model_entities + other_entities
        
        return entities_updated

    @staticmethod
    def merge_BI_entities(message, entities):
        entities_updated = entities
        
        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                if e['entity'].startswith('I-'):
                    temp.append(e)
                else:
                    merged_model_entities.extend(EntityManager.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities

        return entities_updated

    @staticmethod
    def merge_same_entities(message, entities):
        entities_updated = entities
        
        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        tokens = [t for t in message.data["tokens"] if t.text != '__CLS__']

        for token in tokens:
            linked_entity_counter = 0
            for entity in model_entities:
                if token.start == entity['start']:
                    token.linked_entity = entity
                    linked_entity_counter += 1
            if linked_entity_counter > 1:
                print('problem')
                print(tokens)
                print(entities)
                print()
                print(token)
                print()

        merged_model_entities = []
        temp = []
        for token in tokens + [{'token':'dummy',}]:
            if temp == []:
                if hasattr(token, 'linked_entity'):
                    temp.append(token.linked_entity)
                else:
                    continue
            else:
                if hasattr(token, 'linked_entity'):

                    if temp[0]['entity'] == token.linked_entity['entity']:
                        temp.append(token.linked_entity)

                    else:
                        merged_model_entities.extend( EntityManager.base_func_to_merge_entity_subset_without_condition(temp) )
                        
                        temp = []
                        temp.append(token.linked_entity)
                else:
                    merged_model_entities.extend( EntityManager.base_func_to_merge_entity_subset_without_condition(temp) )
                        
                    temp = []

        entities_updated = merged_model_entities + other_entities

        return entities_updated

    @staticmethod
    def merge_custom_entities__money_currency(message, entities):
        entities_updated = entities

        other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
        model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
        model_entities = sorted(model_entities, key=lambda x: x['start'])

        merged_model_entities = []
        model_entities.append({'entity':'dummy', 'value':'dummy',})
        temp = []
        for e in model_entities:
            if temp == []:
                temp.append(e)
            else:
                # if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY','I-AMOUNT-OF-MONEY', 'B-amount', 'I-amount'] and e['entity'] in ['B-currency']:
                if temp[-1]['entity'] in ['B-AMOUNT-OF-MONEY', 'B-amount',] and e['entity'] in ['B-currency']:
                    if 'role' in temp[-1] or 'role' in e:
                        try:
                            assert temp[-1]['role'] == e['role']
                            # merge B-AMOUNT-OF-MONEY/from and B-currency/from, and to-to pair.
                            temp.append(e)
                        except:
                            # do not merge B-AMOUNT-OF-MONEY/from and B-currency/to
                            merged_model_entities.extend(EntityManager.base_func_to_merge_entity_subset(message, temp))        
                            temp = []
                            temp.append(e)
                    else:
                        # merge B-AMOUNT-OF-MONEY and B-currency
                        temp.append(e)
                else:
                    merged_model_entities.extend(EntityManager.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_model_entities + other_entities
        return entities_updated

    @staticmethod
    def merge_custom_entities__account_account__num_currency(message, entities):
        entities_updated = entities

        entities_updated = sorted(entities_updated, key=lambda x: x['start'])
        merged_entities_updated = []
        
        entities_updated.append({'entity':'dummy', 'value':'dummy',})
        
        temp = []
        for e in entities_updated:
            if temp == []:
                temp.append(e)
            else:
                if temp[-1]['entity'] in ['account'] and temp[-1]['extractor'] in ['RegexEntityExtractor'] and e['entity'] in ['account'] and e['extractor'] in ['RegexEntityExtractor']:
                    temp.append(e)
                elif temp[-1]['entity'] in ['<num>'] and temp[-1]['extractor'] in ['RasaSpacyTokenizer'] and e['entity'] in ['B-currency'] and "DIET" in e['extractor']:
                    temp.append(e)
                else:
                    merged_entities_updated.extend(EntityManager.base_func_to_merge_entity_subset(message, temp))        
                    temp = []
                    temp.append(e)


        entities_updated = merged_entities_updated
        return entities_updated
    
    @staticmethod
    def sort_entities_with_config(entities, config):
        ## SORT WITH PRIORITY
        ## KEEP AT LAST IF NOT IN PRIORITY

        entities_updated = entities
        priority_config = config

        temp = []
        tempothers = []
        tempdict = {}
        
        for eidx, entity in enumerate(entities_updated):
            tempdict[eidx] = False

        for priority_i in priority_config:
            for eidx, entity in enumerate(entities_updated):

                if priority_i[0] in entity['extractor'] and priority_i[1] == entity['entity']:
                    temp.append(entity)
                    tempdict[eidx] = True
                    
        for eidx, entity in enumerate(entities_updated):
            if not tempdict[eidx]:
                temp.append(entity)
                
        entities_updated = temp
        temp = []

        return entities_updated

    @staticmethod
    def select_entities_when_multiple(entities):
        ## IF THERE ARE MORE THAN ONE MATCH FOR A TOKEN, SELECT THE FIRST ONE IN PRIORITY 
        ## AFTER FIRST ONE, KEEP IN OTHERS
        entities_updated = entities

        temp = []
        tempspan = []
        tempdict = {}
        
        for entity in entities_updated:
            ## NOTE if 22,25 in tempdict, and an entity with 16,28 comes, 16,28 stays
            overlapidx = -1
            if entity['start'] in tempdict:
                overlapidx = entity['start']
            elif entity['end']-1 in tempdict:
                overlapidx = entity['end']-1

            if overlapidx == -1:
                entity['others'] = []
                temp.append(entity)
                for idx in list(range(entity['start'],entity['end'])):
                    tempdict[idx] = entity
            else:
                tempdict[overlapidx]['others'].append(entity)

        # for entity in entities_updated:
        #     if not (entity['start'] in tempspan or entity['end'] in tempspan):
        #         temp.append(entity)
        #         tempspan.append(entity['start'])
        #         tempspan.append(entity['end'])

        entities_updated = temp
        temp = []

        return entities_updated

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        if not self.priority_config:
            return

        intent = message.get(INTENT)['name']
        entities = message.get("entities", [])
        
        entities_updated = copy.deepcopy(entities)
        priority_config = copy.deepcopy(self.priority_config)

        ############################################################################
        
        if self.component_config["split_same_entities"]:
            entities_updated = EntityManager.split_rasa_entity_merge(entities_updated)
        if self.component_config["merge_BI_entities"]:
            entities_updated = EntityManager.merge_BI_entities(message, entities_updated)
        if self.component_config["merge_same_entities"]:
            entities_updated = EntityManager.merge_same_entities(message, entities_updated)
        
        ############################################################################
        entities_updated = EntityManager.merge_custom_entities__money_currency(message, entities_updated)
        entities_updated = EntityManager.merge_custom_entities__account_account__num_currency(message, entities_updated)
        ############################################################################
        entities_updated = EntityManager.sort_entities_with_config(entities_updated, priority_config)
        entities_updated = EntityManager.select_entities_when_multiple(entities_updated)
        ############################################################################

        message.set("entities", entities_updated, add_to_output=True)


class MCMEntityMapper(Component):
    
    def __init__(self,component_config: Dict[Text, Any] = None,) -> None:
        super(MCMEntityMapper, self).__init__(component_config)
        
        self.dateparser = DateParser(duckling_base_url = 'http://51.124.94.195:8000')

    def process(self, message: Message, **kwargs: Any) -> None:
        intent = message.get(INTENT)
        entities = message.get(ENTITIES, [])

        message.set("raw_entities", entities, add_to_output=True)
        
        entities = self.map_entities(intent['name'], entities)
        message.set("entities", entities, add_to_output=True)
        message.set("mcm_entities", entities, add_to_output=True)
        

    def map_entities(self, intent, entities) -> None:

        def generate_entity(etype, evalue_list):

            if etype in ['history_tr_DATE_SVP_', 'txnlist_tr_DATE_SVP_']:
                output = []
                for evalue in evalue_list:

                    parsed_date = self.dateparser.parse_date(evalue) # dateparser.parse_date("son 3 ay")

                    if parsed_date == []:
                        evalue = 'son 3 ay'
                        parsed_date = self.dateparser.parse_date(evalue)
                        evalue = 'DEFAULT GENERATED'

                    start_date, end_date = parsed_date

                    start_date = f'{start_date[2]}-{"0"*(start_date[1]<10)}{start_date[1]}-{"0"*(start_date[0]<10)}{start_date[0]}T00:00:00Z'
                    end_date = f'{end_date[2]}-{"0"*(end_date[1]<10)}{end_date[1]}-{"0"*(end_date[0]<10)}{end_date[0]}T23:59:59Z'

                    output.append( {
                            'startDate': start_date, 
                            'endDate': end_date, 
                            'tokens': evalue})

                return output

            elif etype in ['history_tr_MODIFIER_SVP__MOD_TR_', 'txnlist_tr_MODIFIER_SVP__MOD_TR_']:
                output = []

                for evalue in evalue_list:
                    temp = xNormalizer.tr_normalize(evalue).lower()

                    if temp in ['en fazla', 'en cok', 'encok', 'en yuksek','en pahali']:
                        output.append({'value': 'MAX'})
                    elif temp in ['en az', 'en dusuk', 'en ucuz']:
                        output.append({'value': 'MIN'})
                    elif temp == 'ortalama':
                        output.append({'value': 'AVG'})
                    elif 'harca' in temp or 'alisveris' in temp:
                        output.append({'value': 'SPEND'})
                
                return output
                    
            else:
                return {
                            'slot': etype,
                            'raw_value': evalue_list,
                            'visual': f"{evalue_list}",
                            'speakable': f"{evalue_list}",
                        }

        def backup_condition(e):

            ## TODO Check suffixes of B-HESAP-X entity for from account. 
            if e['entity'] == 'B-HESAP-X':
                return e['value'] in ['hesabimda', 'hesabımda','hesabimdan', 'hesabımdan', 'hesabimdaki', 'hesabımdaki', 'hesapta', 'hesaptan', 'hesaptaki', ]
            else:
                return False
        
        def remove_words(text, words, suffix=True):
            text = xNormalizer.tr_normalize(text).lower().strip()
            if suffix is True:
                regex = fr'''\b({'|'.join(words)})[a-z]*\b\s*'''
            else:
                regex = fr'''\b({'|'.join(words)})\b\s*'''
            
            return re.sub(regex, '', text).strip()
        
        def remove_substring_elements(elements):
            temp = []
            for e in sorted(elements, key=len, reverse=True):
                tempbool = True
                for tt in temp:
                    if e in tt:
                        tempbool = False
                if tempbool:
                    temp.append(e)
            return temp

        
        entity_blacklist = {
            'account_tr': {
                '_TYPE_': {
                    'with_suffix': ['bakiye', 'hesap', 'hesab'],
                    'exact': ['maxi'],
                }
            },
            'credit_card_tr':{
                '_TYPE_': {
                    'with_suffix': ['kredi', 'kart', 'vadeli', 'vadesiz', 'maas'],
                    'exact': ['maxi'],
                }
                # 'kredi', 
                # 'kart', 'kartim', 'kartımın', 'kartlarımı', 'kartimin', 'kartlarimi', 'kartlarim', 'kartin', 'kartımı',
                # 'kredi kart', 'kredi kartı', 'kredi kartimda', 'kredi karti', 'kredi kartim', 'kredi kartlarım',
                # 'vadeli', 'vadesiz'
            },
            'credit_card_payment_tr':{
                '_CARD_TYPE_TR_': {
                    'with_suffix': ['kredi', 'kart', 'vadeli', 'vadesiz', 'maas'],
                    'exact': ['maxi'],
                }
                # 'kredi', 'kart', 'kredi kart', 'vadeli', 'vadesiz', 'maas', 'kartlarimin', 'kredi kartı', 'Kredi kartı'
            },
            'cash_advance_tr':{
                '_CARD_TYPE_TR_': {
                    'with_suffix': ['kredi', 'kart', 'vadeli', 'vadesiz', 'maas', 'bankamatik', 'atm'],
                    'exact': ['maxi'],
                }
                # 'kredi', 'kart', 'kredi kart', 'vadeli', 'vadesiz'
            },
            'bill_payment_tr':{
                'B-bill-agency':{
                    'exact': ['maxi', 'sen', 'buradan']
                }
            },
            'transfer_money_tr':{
                '_TO_ACCOUNT_TRANSFER_MONEY_TR_':{
                    'exact': ['biten'],
                }
            }
        }

        inform_intents = [
            'inform', # not used in new models

            'inform#recalculation_tr',
            'inform#bill_payment_tr',
            'inform#transfer_money_tr',
            'inform#account_tr',
            'inform#credit_card_tr',
            'inform#term_deposit_calculation_tr',
            'inform#history_tr',
            'inform#foreign_currency_tr',
            'inform#genel_talimat',
        ]
        ner_intents = [
            'account_tr',
            'credit_card_tr',
            'cash_advance_tr',
            'credit_card_payment_tr',
            'foreign_currency_tr',
            'transfer_money_tr',

            'loan_application_tr',
            'term_deposit_calculation_tr',

            'bill_payment_tr',

            'history_tr',
            'txnlist_tr',

            'spendadvice_tr',
            'campaign_tr',

            'ustu_kalsin',
            ]

        if intent not in ner_intents + inform_intents:
            return {}
            pass
        
        elif intent in inform_intents:
            output = {}
            for ni in ner_intents:
                output[ni] = self.map_entities(ni, entities)
            entities = output

        elif intent == 'account_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', ]

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TYPE_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    pass
                elif 'DIET' in e['extractor']:
                    if e['entity'] == 'B-account':
                    
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['account_tr']['_TYPE_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['account_tr']['_TYPE_']['with_suffix'])
                        if e_value == '':
                            continue

                        output['_TYPE_'].append(e_value)
                        checks['_TYPE_'] = True
                    elif e['entity'] == 'B-sube':
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True
                    elif e['entity'] == 'B-currency':
                        output['_TYPE_'].append(e['value'])
                        checks['_TYPE_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TYPE_'] and e['entity'] == 'account':
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['account_tr']['_TYPE_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['account_tr']['_TYPE_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_TYPE_'].append(e_value)
                    
                elif 'DIET' in e['extractor']:
                    pass
                    # if not checks['_TYPE_'] and e['entity'] == 'B-HESAP-X': # and backup_condition(e) # Not needed in this intent.
                    #     output['_TYPE_'].append(e['value'])

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'credit_card_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', ]

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TYPE_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    pass
                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-account', 'B-cardtype', 'B-CARDTYPE']:
                        
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_TYPE_'].append(e_value)
                        checks['_TYPE_'] = True
                    elif e['entity'] in ['B-currency']:


                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_TYPE_'].append(e_value)
                        checks['_TYPE_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TYPE_'] and e['entity'] == 'account':
                        
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['credit_card_tr']['_TYPE_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_TYPE_'].append(e_value)
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'cash_advance_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CARD_TYPE_TR_', '_AMOUNT_TR_','_INSTALLMENT_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_CARD_TYPE_TR_':False, '_AMOUNT_TR_':False,'_INSTALLMENT_TR_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CARD_TYPE_TR_':[], '_AMOUNT_TR_':[], '_INSTALLMENT_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        output['_AMOUNT_TR_'].append(e['text'])
                        checks['_AMOUNT_TR_'] = True

                elif 'DIET' in e['extractor']:
                    # 'B-account' # kredi karti, vadesiz
                    if e['entity'] in ['B-cardtype', 'B-CARDTYPE', 'B-account']:
                        
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['cash_advance_tr']['_CARD_TYPE_TR_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['cash_advance_tr']['_CARD_TYPE_TR_']['with_suffix'])
                        
                        if e_value == '':
                            continue
                            
                        output['_CARD_TYPE_TR_'].append(e_value)
                        checks['_CARD_TYPE_TR_'] = True
                    elif e['entity'] in ['B-DATE-DURATION']:
                        tempinstallment = e['value']
                        tempinstallment = re.sub('((taksit|ayl[iı]k).*?|ay)($|\s)', '', tempinstallment).strip()
                        output['_INSTALLMENT_TR_'].append(tempinstallment)

                    elif e['entity'] in ['B-amount', 'B-AMOUNT-OF-MONEY']:
                        output['_AMOUNT_TR_'].append(e['value'])
                        checks['_AMOUNT_TR_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    if not checks['_CARD_TYPE_TR_'] and e['entity'] == 'account':
                        
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['cash_advance_tr']['_CARD_TYPE_TR_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['cash_advance_tr']['_CARD_TYPE_TR_']['with_suffix'])
                        
                        if e_value == '':
                            continue
                        output['_CARD_TYPE_TR_'].append(e_value)
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'credit_card_payment_tr':
           
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CARD_TYPE_TR_', '_AMOUNT_TR_', '_PAYMENT_TYPE_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_CARD_TYPE_TR_':False, '_AMOUNT_TR_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CARD_TYPE_TR_':[], '_AMOUNT_TR_':[], '_PAYMENT_TYPE_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        output['_AMOUNT_TR_'].append(e['text'])
                        checks['_AMOUNT_TR_'] = True

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-account', 'B-cardtype', 'B-CARDTYPE']:

                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['credit_card_payment_tr']['_CARD_TYPE_TR_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['credit_card_payment_tr']['_CARD_TYPE_TR_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_CARD_TYPE_TR_'].append(e_value)
                        checks['_CARD_TYPE_TR_'] = True

                    elif e['entity'] in ['B-TEXT-AMOUNT']:
                        output['_PAYMENT_TYPE_TR_'].append(e['value'])

                    elif e['entity'] in ['B-amount', 'B-AMOUNT-OF-MONEY']:
                        output['_AMOUNT_TR_'].append(e['value'])
                        checks['_AMOUNT_TR_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    if not checks['_CARD_TYPE_TR_'] and e['entity'] == 'account':
                    
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['credit_card_payment_tr']['_CARD_TYPE_TR_']['exact'], suffix=False)
                        e_value = remove_words(e_value, entity_blacklist['credit_card_payment_tr']['_CARD_TYPE_TR_']['with_suffix'])
                        
                        if e_value == '':
                            continue

                        output['_CARD_TYPE_TR_'].append(e_value)
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
                      
        elif intent == 'foreign_currency_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            
            val = ['_TARGET_AMOUNT_TR_', '_REF_AMOUNT_TR_', 
            '_BUY_TR_', '_SELL_TR_']

            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_TARGET_AMOUNT_TR_':False, '_REF_AMOUNT_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TARGET_AMOUNT_TR_':[], '_REF_AMOUNT_TR_':[],
            '_BUY_TR_':[], '_SELL_TR_':[]}
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        # TODO Duckling losts to / from information.
                        output['_TARGET_AMOUNT_TR_'].append(e['text'])
                        checks['_TARGET_AMOUNT_TR_'] = True
                elif 'DIET' in e['extractor']:

                    if 'role' in e and e['role'] == 'to':
                        output['_TARGET_AMOUNT_TR_'].append(e['value'])
                        checks['_TARGET_AMOUNT_TR_'] = True

                    elif 'role' in e and e['role'] == 'from':
                        output['_REF_AMOUNT_TR_'].append(e['value'])
                        checks['_REF_AMOUNT_TR_'] = True

                    elif e['entity'] in ['B-amount', 'B-AMOUNT-OF-MONEY']:
                        
                        # try:
                        #     assert e['raw'][-1]['entity'] == 'B-currency'
                        #     assert len(e['raw']) == 2
                        #     assert re.findall(r'(tl|lira|dolar|usd|euro|eur|yüro|avro|\$|€|pound|sterlin|gbp)', e['raw'][0]['raw'][-1]['value'])
                        #     output['_REF_AMOUNT_TR_'].append(e['raw'][0]['value'])
                        #     output['_TARGET_AMOUNT_TR_'].append(e['raw'][-1]['value'])
                        # except:
                        #     output['_TARGET_AMOUNT_TR_'].append(e['value'])

                        output['_TARGET_AMOUNT_TR_'].append(e['value'])
                        checks['_TARGET_AMOUNT_TR_'] = True

                    elif e['entity'] in ['B-BUY-X', 'B-EXCHANGE-X', 'B-SEND-X']:
                        # TODO B-EXCHANGE-X and B-SEND-X can also belong to B-SELL-X.
                        # TODO TODO
                        
                        if xNormalizer.tr_normalize(e['value']).lower().strip() in ['kur', 'kuru', 'vurdu', 'ulasti']:
                            continue
                        output['_BUY_TR_'].append(e['value'])
                        
                    elif e['entity'] in ['B-SELL-X']: 
                    
                        if xNormalizer.tr_normalize(e['value']).lower().strip() in ['kur', 'kuru', 'vurdu', 'ulasti']:
                            continue
                        output['_SELL_TR_'].append(e['value'])

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    pass
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    if not checks['_TARGET_AMOUNT_TR_'] and e['entity'] == '<num>':
                        output['_TARGET_AMOUNT_TR_'].append(e['value'])

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-currency']:
                        if not checks['_REF_AMOUNT_TR_'] and not checks['_TARGET_AMOUNT_TR_']:
                            output['_TARGET_AMOUNT_TR_'].append(e['value'])
                            
            # UPDATE REF AND TARGET FOR MCM
            # if output['_BUY_TR_'] == []:
            if output['_SELL_TR_'] != [] and output['_BUY_TR_'] == []:
                if output['_REF_AMOUNT_TR_'] != []:
                    temppostprocessing = output['_TARGET_AMOUNT_TR_']
                    output['_TARGET_AMOUNT_TR_'] = output['_REF_AMOUNT_TR_']
                    output['_REF_AMOUNT_TR_'] = temppostprocessing

            if output['_REF_AMOUNT_TR_'] != [] and output['_TARGET_AMOUNT_TR_'] != [] and any([re.findall(r'(\b|\s|^)(tl|lira)', v) for v in output['_TARGET_AMOUNT_TR_']]):
                    temppostprocessing = output['_TARGET_AMOUNT_TR_']
                    output['_TARGET_AMOUNT_TR_'] = output['_REF_AMOUNT_TR_']
                    output['_REF_AMOUNT_TR_'] = temppostprocessing

            ###
            target_copy = copy.deepcopy(output['_TARGET_AMOUNT_TR_'])
            for v in target_copy:
                if re.findall(r'(\b|\s|^|\d)(tl|lira)', v):
                    if '_REF_AMOUNT_TR_' not in output:
                        output['_REF_AMOUNT_TR_'] = []
                    output['_TARGET_AMOUNT_TR_'].remove(v)
                    output['_REF_AMOUNT_TR_'].append(v)
                    
            ###
            target_copy = copy.deepcopy(output['_TARGET_AMOUNT_TR_'])
            for v in target_copy:
                if re.findall(r'(dolar|usd|euro|sterlin|gbp|avro)', v) and re.findall(r'(doviz)', v):
                    output['_TARGET_AMOUNT_TR_'].remove(v)
                    output['_TARGET_AMOUNT_TR_'].append(re.sub(r'\bdoviz[a-z]*\b','',v).strip())


            output['_REF_AMOUNT_TR_'] = remove_substring_elements(output['_REF_AMOUNT_TR_'])
            output['_TARGET_AMOUNT_TR_'] = remove_substring_elements(output['_TARGET_AMOUNT_TR_'])

            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'transfer_money_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_AMOUNT_TRANSFER_MONEY_TR_', 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_', 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_', 
            '_TRXTYPE_TRANSFER_MONEY_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_TRANSFER_MONEY_TR_':False, 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_':False, 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_AMOUNT_TRANSFER_MONEY_TR_':[], 
            '_TO_ACCOUNT_TRANSFER_MONEY_TR_':[], 
            '_FROM_ACCOUNT_TRANSFER_MONEY_TR_':[], 
            '_TRXTYPE_TRANSFER_MONEY_TR_':[]}
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        output['_AMOUNT_TRANSFER_MONEY_TR_'].append(e['text'])
                        checks['_AMOUNT_TRANSFER_MONEY_TR_'] = True

                elif 'DIET' in e['extractor']:
                    if e['entity'] == 'B-per':
                        # TODO No need to check 'to' / 'from'. It must be a 'to'.
                        
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif 'role' in e and e['role'] == 'to':
                    
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif 'role' in e and e['role'] == 'from':
                    
                        output['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'] = True

                    elif e['entity'] == 'B-txtype':
                        output['_TRXTYPE_TRANSFER_MONEY_TR_'].append(e['value'])

                    elif e['entity'] == 'B-bank':
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            
            for e in entities:
                if 'DIET' in e['extractor']:
                    if e['entity'] in ['B-AMOUNT-OF-MONEY']:   
                        if not checks['_AMOUNT_TRANSFER_MONEY_TR_']:
                            output['_AMOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                            checks['_AMOUNT_TRANSFER_MONEY_TR_'] = True

                    elif e['entity'] in ['B-currency']:
                        ## TODO improve
                        output['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
                        checks['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'] = True

            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TO_ACCOUNT_TRANSFER_MONEY_TR_'] and e['entity'] in ['B-female-name', 'B-male-name', 'B-last-name']:
                    
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['transfer_money_tr']['_TO_ACCOUNT_TRANSFER_MONEY_TR_']['exact'], suffix=False)
                        if e_value == '':
                            continue
                            
                        output['_TO_ACCOUNT_TRANSFER_MONEY_TR_'].append(e_value)

                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    if not checks['_AMOUNT_TRANSFER_MONEY_TR_'] and e['entity'] == '<num>':
                        output['_AMOUNT_TRANSFER_MONEY_TR_'].append(e['value'])

                elif 'DIET' in e['extractor']:
                    ## TODO Check suffixes of B-HESAP-X entity for from account. 
                    if not checks['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'] and e['entity'] == 'B-HESAP-X' and backup_condition(e):
                        output['_FROM_ACCOUNT_TRANSFER_MONEY_TR_'].append(e['value'])
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'loan_application_tr':
            
               
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CURRENCY_', '_AMOUNT_', 
            '_CREDIT_TYPE_',
            '_DATE_MONTH_', '_DATE_YEAR_','_DATE_DAY_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CURRENCY_':[], '_AMOUNT_':[], 
            '_CREDIT_TYPE_':[],
            '_DATE_MONTH_':[], '_DATE_YEAR_':[],'_DATE_DAY_':[],
            '_RECALCULATION_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency
                        output['_CURRENCY_'].append(tempcurrency)
                        output['_AMOUNT_'].append(str(e['additional_info']['value']))
                        checks['_AMOUNT_'] = True

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-DURATION']:
                        if 'role' in e:
                            if e['role'] in ['YEAR']:
                                output['_DATE_YEAR_'].append(e['value'])
                            elif e['role'] in ['MONTH']:
                                output['_DATE_MONTH_'].append(e['value'])
                            elif e['role'] in ['DAY']:
                                output['_DATE_DAY_'].append(e['value'])
                        else:
                            print(e)
                            print('B-DURATION does not have role.')
                    elif e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            output['_AMOUNT_'].append(e['raw'][0]['value'])
                            output['_CURRENCY_'].append(e['raw'][-1]['value'])
                        except:
                            output['_AMOUNT_'].append(e['value'])
                        checks['_AMOUNT_'] = True
                    elif e['entity'] in ['B-CREDITTYPE']:
                        output['_CREDIT_TYPE_'].append(e['value'])

                    elif e['entity'] in ['B-CALCULATE']:
                        output['_RECALCULATION_'].append(e['value'])


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]

        elif intent == 'term_deposit_calculation_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_TYPE_', '_AMOUNT_', 
            '_DATE_MONTH_', '_DATE_YEAR_','_DATE_DAY_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False, '_TYPE_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TYPE_':[], '_AMOUNT_':[], 
            '_DATE_MONTH_':[], '_DATE_YEAR_':[],'_DATE_DAY_':[],
            '_RECALCULATION_':[], }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency
                        output['_TYPE_'].append(tempcurrency)
                        output['_AMOUNT_'].append(str(e['additional_info']['value']))
                        checks['_AMOUNT_'] = True

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            output['_AMOUNT_'].append(e['raw'][0]['value'])
                            output['_TYPE_'].append(e['raw'][-1]['value'])
                        except:
                            output['_AMOUNT_'].append(e['value'])
                        checks['_AMOUNT_'] = True

                        
                    elif e['entity'] in ['B-DURATION']:
                        if 'role' in e:
                            if e['role'] in ['YEAR']:
                                output['_DATE_YEAR_'].append(e['value'])
                            elif e['role'] in ['MONTH']:
                                output['_DATE_MONTH_'].append(e['value'])
                            elif e['role'] in ['DAY']:
                                output['_DATE_DAY_'].append(e['value'])
                        else:
                            print(e)
                            print('B-DURATION does not have role.')
                    
                    elif e['entity'] in ['B-currency']:
                        output['_TYPE_'].append(e['value'])

                    elif e['entity'] in ['B-CALCULATE']:
                        output['_RECALCULATION_'].append(e['value'])

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:

                    if e['entity'] in ['B-DURATION-X']:
                        if 'role' in e:
                            if e['role'] in ['YEAR']:
                                if output['_DATE_YEAR_'] == []:
                                    output['_DATE_YEAR_'].append(e['value'])
                            elif e['role'] in ['MONTH']:
                                if output['_DATE_MONTH_'] == []:
                                    output['_DATE_MONTH_'].append(e['value'])
                            elif e['role'] in ['DAY']:
                                if output['_DATE_DAY_'] == []:
                                    output['_DATE_DAY_'].append(e['value'])
                        else:
                            print(e)
                            print('B-DURATION-X does not have role.')

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'bill_payment_tr':

            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_ACCOUNT_TR_', '_TARGET_TR_', '_CATEGORY_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_ACCOUNT_TR_':False, '_TARGET_TR_':False, '_CATEGORY_TR_':False, }

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_ACCOUNT_TR_':[], '_TARGET_TR_':[], '_CATEGORY_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    pass
                
                elif 'DIET' in e['extractor']:
                    if e['entity'] == 'B-account':
                        # TODO No need to check 'to' / 'from'. It must be a 'from'.
                        output['_ACCOUNT_TR_'].append(e['value'])
                        checks['_ACCOUNT_TR_'] = True
                    elif e['entity'] == 'B-bill-agency':
                    
                        e_value = e['value']
                        e_value = remove_words(e_value, entity_blacklist['bill_payment_tr']['B-bill-agency']['exact'], suffix=False)
                        if e_value == '':
                            continue
                            
                        output['_TARGET_TR_'].append(e_value)
                        checks['_TARGET_TR_'] = True
                    elif e['entity'] == 'B-bill-type':
                        output['_CATEGORY_TR_'].append(e['value'])
                        checks['_CATEGORY_TR_'] = True

            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':
                    if not checks['_TARGET_TR_'] and e['entity'] in ['B-billing-agencies']:
                        output['_TARGET_TR_'].append(e['value'])
                    
                    elif not checks['_ACCOUNT_TR_'] and e['entity'] == 'account':
                        output['_ACCOUNT_TR_'].append(e['value'])
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    ## TODO Check suffixes of B-HESAP-X entity for from account. 
                    if not checks['_ACCOUNT_TR_'] and e['entity'] == 'B-HESAP-X' and backup_condition(e):
                        output['_ACCOUNT_TR_'].append(e['value'])

            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output
            # entities = [generate_entity(k, output[k]) for k in output if output[k] != []]
            
        elif intent == 'history_tr':
                       
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_ACCOUNT_SVP_', '_DATE_SVP_', '_DATE_', 
            '_MODIFIER_SVP_', '_MOD_TR_', '_TARGET_SVP_',]
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_AMOUNT_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_DATE_SVP_':[], '_DATE_':[], 
            '_MOD_ORDER_':[], '_MODIFIER_SVP_':[], '_MOD_TR_':[],
            '_ACCOUNT_SVP_':[],'_TARGET_SVP_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        pass

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-target_svp', 'B-SPENDING-CATEGORY']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-date_svp']:
                        output['_DATE_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-modifier_svp']:
                        output['_MODIFIER_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-account_svp', 'B-account']:
                        output['_ACCOUNT_SVP_'].append(e['value'])

                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            if output['_DATE_SVP_'] != []:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', output['_DATE_SVP_']) 
            else:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', ['son 3 ay'])
                output['_DATE_'][0]['tokens'] = 'DEFAULT GENERATED'

            if output['_MODIFIER_SVP_'] != []:
                output['_MOD_TR_'] = generate_entity(f'{intent}_MODIFIER_SVP__MOD_TR_', output['_MODIFIER_SVP_']) 
            
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'txnlist_tr':
            
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            
            val = ['_ACCOUNT_SVP_', '_DATE_SVP_', '_DATE_', 
            '_LOCATION_SVP_',  
            '_MONEY_MAX_SVP_', '_MONEY_MIN_SVP_', '_COUNT_SVP_', 
            '_MODIFIER_SVP_', '_MOD_TR_','_TARGET_SVP_',
            ]
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_DATE_SVP_':[], '_DATE_':[], 
            '_MOD_ORDER_':[], '_MODIFIER_SVP_':[], '_MOD_TR_':[],
            '_ACCOUNT_SVP_':[],'_TARGET_SVP_':[],
            '_LOCATION_SVP_':[],
            '_MONEY_MAX_SVP_':[], '_MONEY_MIN_SVP_':[], 
            '_COUNT_SVP_':[], '_COUNT_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        pass

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-target_svp', 'B-SPENDING-CATEGORY']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-date_svp']:
                        output['_DATE_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-modifier_svp']:
                        output['_MODIFIER_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-account_svp', 'B-account']:
                        output['_ACCOUNT_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-count_svp']:
                        output['_COUNT_SVP_'].append(e['value'])
                        try:
                            output['_COUNT_'].append(int(e['value']))
                        except:
                            pass
                    elif e['entity'] in ['B-money_min_svp']:
                        output['_MONEY_MIN_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-money_max_svp']:
                        output['_MONEY_MAX_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-location_svp']:
                        output['_LOCATION_SVP_'].append(e['value'])

                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            if output['_DATE_SVP_'] != []:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', output['_DATE_SVP_'])
            else:
                output['_DATE_'] = generate_entity(f'{intent}_DATE_SVP_', ['son 3 ay'])
                output['_DATE_'][0]['tokens'] = 'DEFAULT GENERATED'
                
            if output['_MODIFIER_SVP_'] != []:
                output['_MOD_TR_'] = generate_entity(f'{intent}_MODIFIER_SVP__MOD_TR_', output['_MODIFIER_SVP_']) 
            
            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'spendadvice_tr':
            
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_TARGET_SVP_','_MONEY_', '_AMOUNT_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_TARGET_SVP_':[], '_MONEY_':[], '_AMOUNT_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        
                        tempcurrency = e['additional_info']['unit']
                        tempcurrency = 'lira' if tempcurrency == 'TRY' else tempcurrency

                        output['_AMOUNT_TR_'].append(e['text'])
                        output['_MONEY_'].append({
                            'tokens': e['text'], 
                            'numbers': [{'value': e['value'], 'tokens': str(e['value'])}], 
                            'value': e['value'], 
                            'currency': tempcurrency, 
                            'svp_tokens': e['text']})

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-SPENDING-CATEGORY']:
                        output['_TARGET_SVP_'].append(e['value'])
                    elif e['entity'] in ['B-AMOUNT-OF-MONEY']:
                        
                        try:
                            tempcurrencybool = e['raw'][-1]['entity'] == 'B-currency'
                            assert tempcurrencybool
                            assert len(e['raw']) == 2
                            
                            tempall = e['value']
                            tempamount = e['raw'][0]['value']
                            tempcurrency = e['raw'][-1]['value']
                        except:
                            tempall = e['value']
                            tempamount = e['value']
                            tempcurrency = e['value']

                        output['_AMOUNT_TR_'].append(tempall)
                        output['_MONEY_'].append({
                            'tokens': tempall, 
                            'numbers': [{'value': tempamount, 'tokens': str(tempamount)}], 
                            'value': tempamount, 
                            'currency': tempcurrency, 
                            'svp_tokens': tempall})

                        # output['_MONEY_'].append({
                        #     'tokens': e['value'], 
                        #     'numbers': [{'value': e['value'], 'tokens': str(e['value'])}], 
                        #     'value': e['value'], 
                        #     'currency': e['value'], 
                        #     'svp_tokens': e['value']})


                        


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'campaign_tr':

            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            # '_DATE_START_', '_DATE_END_', '_MOD_ORDER_', 
            val = ['_JOINED_TR_','_TARGET_TR_','_STAFF_TR_']
            
            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_JOINED_TR_':[], '_TARGET_TR_':[], '_STAFF_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        pass

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-JOIN-X']:
                        output['_JOINED_TR_'].append(e['value'])
                    elif e['entity'] in ['B-SPENDING-CATEGORY']:
                        output['_TARGET_TR_'].append(e['value'])
                    elif e['entity'] in ['B-STAFF-X']:
                        output['_STAFF_TR_'].append(e['value'])
            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':                    
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        elif intent == 'ustu_kalsin':
           
            ############################
            ## MCM EXPECTED ENTITIES
            ############################
            val = ['_CARD_TYPE_TR_', '_AMOUNT_TR_', '_PROCESS_TYPE_TR_', '_ACCOUNT_TR_']

            ############################
            ## OUTPUT CONTROL BOOLEANS
            ############################
            checks ={'_CARD_TYPE_TR_':False, '_AMOUNT_TR_':False, '_ACCOUNT_TR_':False}

            
            ############################
            ## OUTPUT VARIABLE
            ############################
            output = {'_CARD_TYPE_TR_':[], '_AMOUNT_TR_':[], '_PROCESS_TYPE_TR_':[], '_ACCOUNT_TR_':[] }
            
            ############################
            ## MAIN ENTITIES
            ############################
            for e in entities:
                if 'Duckling' in e['extractor']:
                    
                    if e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus']:
                        output['_AMOUNT_TR_'].append(e['text'])
                        checks['_AMOUNT_TR_'] = True

                elif 'DIET' in e['extractor']:
                    if e['entity'] in ['B-CARDTYPE']:

                        e_value = e['value']
                        # e_value = remove_words(e_value, entity_blacklist['ustu_kalsin']['_CARD_TYPE_TR_']['exact'], suffix=False)
                        # e_value = remove_words(e_value, entity_blacklist['ustu_kalsin']['_CARD_TYPE_TR_']['with_suffix'])
                        # if e_value == '':
                        #     continue

                        output['_CARD_TYPE_TR_'].append(e_value)
                        checks['_CARD_TYPE_TR_'] = True

                    elif e['entity'] in ['B-PROCESS-X']:
                        output['_PROCESS_TYPE_TR_'].append(e['value'])

                    elif e['entity'] in ['B-amount', 'B-AMOUNT-OF-MONEY']:
                        output['_AMOUNT_TR_'].append(e['value'])
                        checks['_AMOUNT_TR_'] = True

                    elif e['entity'] in ['B-account', 'B-sube']:
                        output['_ACCOUNT_TR_'].append(e['value'])
                        checks['_ACCOUNT_TR_'] = True


            ############################
            ## BACKUP ENTITIES
            ############################
            for e in entities:
                if e['extractor'] ==  'RegexEntityExtractor':      
                    pass
                        
                elif e['extractor'] ==  'RasaSpacyTokenizer':
                    pass
                
                elif 'DIET' in e['extractor']:
                    pass

            
            [output.pop(k) for k in list(output.keys()) if output[k] == []]
            entities = output

        else:
            print(f"This intent is not handled : {intent}")

        return entities


class PostProcessing(Component):
    defaults = {
        "train_training_data_processors" : [],
        "train_message_processors" : [],
        "predict_message_processors" : [],
    }

    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(PostProcessing, self).__init__(component_config)

    ##################################################################

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for processor in self.component_config["train_training_data_processors"]:
            self.training_data_processor_func(training_data, processor=processor)

        for processor in self.component_config["train_message_processors"]:
            for message in training_data.training_examples:
                self.message_processor_func(message, processor=processor)

    def process(self, message: Message, **kwargs: Any) -> None:

        for processor in self.component_config["predict_message_processors"]:
            self.message_processor_func(message, processor=processor)

    ##################################################################

    def message_mapping_base(self, message, message_intent, message_2nd_intent, 
                            mode, rule, source_intent, target_intent, target_entities ):
        
        def update_message(message, target_intent, target_entities):
            message.set(INTENT, {'name': target_intent, 'confidence': 0.998})
            if target_entities is not False:
                message.set("entities", target_entities)
                message.set("mcm_entities", target_entities)

        if message_intent['name'] != source_intent:
            return False

        if mode == 'match':

            if re.match(rule['regex'], message.text):
                update_message(message, target_intent, target_entities)
                return True
            else:
                return False

        elif mode == 'findall':
            if bool(re.findall(rule['regex'], message.text)):
                update_message(message, target_intent, target_entities)
                return True
            else:
                return False

        elif mode == '2nd_score':
            
            if message_2nd_intent['name'] == target_intent and message_2nd_intent['confidence'] > rule['confidence'] :
                update_message(message, target_intent, target_entities)
                return True
            else:        
                return False

    def message_mapping_func(self, message, mapping_config ):

        intent = message.get(INTENT)
        intent_ranking = message.get('intent_ranking')
        
        for m in mapping_config:
            matched = self.message_mapping_base(message, intent, intent_ranking[1], 
                            m[0],m[1],m[2],m[3],m[4],) # mode, rule, source_intent, target_intent, target_entities
            if matched:
                break

    ##################################################################

    def training_data_processor_func(self, training_data, processor='display_diet_attribute'):
        
        if processor == "display_diet_attribute":
            count = 5
            for message in training_data.training_examples:
                if count == 0 :
                    continue
                entities = message.get('diet')
                if entities is not None:
                    count = count - 1
                    print(entities)

    def message_processor_func(self, message, processor='maxi'):
        # message.text

        # intent = message.get(INTENT)
        # entities = message.get(ENTITIES, [])
        
        # intent['name'], intent['confidence]
        # entity['extractor'], entity['entity'], entity['value']

        # message.set(INTENT, {'name': 'my_earnings_tr', 'confidence': 0.998})
        # message.set("entities", {})
        # message.set("entities", entities, add_to_output=True)

        if processor == 'maxi':
        
            # mode, rule, source_intent, target_intent, target_entities
            mapping_config = [
                
                # 2018 maxipuan
                ('findall', {'regex':r'2018.*puan'}, 'credit_card_tr', 'my_earnings_tr', {}),
                ('findall', {'regex':r'puan.*2018'}, 'credit_card_tr', 'my_earnings_tr', {}),
                

                # kıredi kartımın kulana bilir bakiye nedir 	credit_card_tr 	card_application_track_tr
                ('match', {'regex':r'^k[a-z]* kart[a-z]* kul[a-z]*( bil[a-z]*){0,1} baki[a-z]*( ned[a-z]*){0,1} .$'}, 'card_application_track_tr', 'credit_card_tr', {}),
                # ben de sizden çok mutluyum    good_comment_tr 	i_am_upset_tr
                ('match', {'regex':r'^.* mutlu[a-z]* .$'}, 'i_am_upset_tr', 'good_comment_tr', {}),
                # kredi kartı bilgilerini öğrenmek istiyorum    credit_card_tr 	card_info_tr
                ('findall', {'regex':r'^k.{0,1}redi kart[a-z]* bilgi'}, 'card_info_tr', 'credit_card_tr', {}),
                # hesaptan para 	transfer_money_tr 	cross_account_transfer_tr
                ('match', {'regex':r'^hes[a-z]*an para[a-z]* .$'}, 'cross_account_transfer_tr', 'transfer_money_tr', {}),
                # halk bankasına para göndermek istiyorum 	transfer_money_tr 	baskabanka_kkr_odeme
                ('match', {'regex':r'^halk.{0,1}bank[a-z]*( para[a-z]*){0,1} gond[a-z]*( isti[a-z]*) .$'}, 'baskabanka_kkr_odeme', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['halk']}),
                # merhaba Medineye para göndereceğim 	transfer_money_tr 	greetings_tr
                ('match', {'regex':r'^merh[a-z]* medine[a-z]* para gond[a-z]* .$'}, 'greetings_tr', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['medine']}),
                # ulaşa 300 tl gönder 	transfer_money_tr 	prepaid_line_tr
                ('match', {'regex':r'^ulas[a-z]* (\d* ){0,1}(tl|lira|para) gond[a-z]* .$'}, 'prepaid_line_tr', 'transfer_money_tr', {'_TO_ACCOUNT_TRANSFER_MONEY_TR_': ['ulas']}),
                # tuçe bagay tarafından gönderilen toplam para 	txnlist_tr 	oos
                ('match', {'regex':r'^([a-z]* ){0,3}gond[a-z]*( (toplam|butun)){0,1} para .$'}, 'oos', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-11-04T00:00:00Z','endDate': '2021-03-04T23:59:59Z','tokens': 'DEFAULT GENERATED'}],'_MODIFIER_SVP_': ['gonderilen'],}),
                # hacı fırat aksoy den gelen havale eder 	txnlist_tr 	eft_time_tr
                ('match', {'regex':r'^([a-z]* ){0,4}gel[a-z]* havale[a-z]*( eder){0,1} .$'}, 'eft_time_tr', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-11-04T00:00:00Z','endDate': '2021-03-04T23:59:59Z','tokens': 'DEFAULT GENERATED'}],'_MODIFIER_SVP_': ['gelen'],'_TARGET_SVP_': ['havale']}),
                # canlı biri var mı 	customer_representative_tr 	6a1a17
                ('match', {'regex':r'^canli biri( var){0,1}( mi){0,1} .$'}, '6a1a17', 'customer_representative_tr', {}),
                # hesap limitim ne kadar
                ('match', {'regex':r'^hesap limit[a-z]*( ne[a-z]*){0,1}( kadar[a-z]*){0,1} .$'}, 'credit_card_tr', 'account_tr', {}),


                # ekstre hesap borcumu hesabımdaki paradan öde
                ('findall', {'regex':r'ekstre'}, 'overdraft_debt_payment_tr', 'credit_card_payment_tr', False),

                # şuan borç tutarım 
                # ('match', {'regex':r'^suan[a-z]* borc[a-z]* tutar[a-z]* .$'}, 'credit_card_tr', 'upcoming_payments_tr', {}),
                # şuan güncel borcum ne kadar
                # ('match', {'regex':r'^suan[a-z]* guncel[a-z]* borc[a-z]* ne[a-z]*( kadar[a-z]*){0,1} .$'}, 'credit_card_tr', 'upcoming_payments_tr', {}),

                # Kredi kartımın genel borcu
                # ('match', {'regex':r'^kredi[a-z]* kart[a-z]* genel[a-z]* borc[a-z]* .$'}, 'credit_card_payment_tr', 'credit_card_tr', {}),

                # ana menüye git
                ('match', {'regex':r'^ana[a-z]* menu[a-z]* git[a-z]* .$'}, 'ana_menu', 'open_iscep_tr', {}),

                # şuan alışveriş yapabilir miyim
                # ('match', {'regex':r'^suan[a-z]* alisv[a-z]* yap[a-z]*( m[a-z]*){0,1} .$'}, 'online_shopping_tr', 'spendadvice_tr', {'_TARGET_SVP_': ['alisveris']}),

                # Şu kartım için harcama tavsiyesi ver
                # ('findall', {'regex':r'harcama[a-z]* tavsiye[a-z]*'}, 'history_tr', 'spendadvice_tr', {}),

                # havale nasıl yapılır 
                # ('match', {'regex':r'^havale[a-z]* nasil[a-z]* yap[a-z]* .$'}, 'remittance_identify_tr', 'transfer_money_tr', False),

                # bu ay ne kadar kazandım
                # ('findall', {'regex':r'\bkazan'}, 'history_tr', 'txnlist_tr', False),

                # çağrı merkezinden birileriyle görüşebilir miyim
                # ('match', {'regex':r'^cagri[a-z]* merkez[a-z]* .*gorus[a-z]* .*.$'}, 'telefon_numarasi', 'customer_representative_tr', False),
                # beni çağrıya aktar
                # ('match', {'regex':r'^.*cagri[a-z]* aktar[a-z]* .*.$'}, 'telefon_numarasi', 'customer_representative_tr', False),
                # beni çağrıya aktarir misin
                # ('match', {'regex':r'^beni cagri[a-z]* .*aktar[a-z]* .*.$'}, 'transfer_money_tr', 'customer_representative_tr', {}),

                # diger gelir
                # ('match', {'regex':r'^diger[a-z]* gelir[a-z]* .$'}, 'transfer_to_undefined_account_tr', 'txnlist_tr', {'_DATE_SVP_': ['bu ayki'], '_DATE_': [{'startDate': '2021-01-01T00:00:00Z', 'endDate': '2021-01-31T23:59:59Z', 'tokens': 'bu ayki'}],'_MODIFIER_SVP_': ['gelirlerim']}),

                # vadesi euro hesabimi sat
                # ('match', {'regex':r'^vades[a-z]* euro[a-z]* hes[a-z]* sat[a-z]* .$'}, 'account_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['euro'], '_SELL_TR_': ['sat']}),
                # ('match', {'regex':r'^vades[a-z]* euro[a-z]* hes[a-z]* al[a-z]* .$'}, 'account_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['euro'], '_BUY_TR_': ['al']}),
                # ('match', {'regex':r'^vade[a-z]* dolar[a-z]* hes[a-z]* sat[a-z]* .$'}, 'account_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['dolar'], '_SELL_TR_': ['sat']}),
                # ('match', {'regex':r'^vade[a-z]* dolar[a-z]* hes[a-z]* al[a-z]* .$'}, 'account_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']}),

                # euro nekadar
                # ('match', {'regex':r'^euro[a-z]* ne[a-z]*kadar[a-z]* .$'}, 'account_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['euro']}),

                # Kredi kartı askeriyesi ne kadar
                # ('findall', {'regex':r'askeri'}, 'credit_card_tr', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['askeri']}),

                # borç versene
                # ('match', {'regex':r'^borc ver[a-z]*( misin)* .$'}, 'debt_config_tr', 'cash_advance_tr', False),

                # Kart bilgilerim çalındı
                # ('match', {'regex':r'^kart bilgi[a-z]* cal[a-z]* .$'}, 'card_info_tr', 'lost_stolen_card_tr', False),

                # kredi başvuru ayrıntıları
                # ('match', {'regex':r'^kredi[a-z]* basvuru[a-z]* ayrinti[a-z]* .$'}, '2a2a4', 'credit_application_track_tr', False),

                # eft masrafı
                # ('match', {'regex':r'^eft masraf[a-z]* .$'}, '6a6a13', 'price_rates_tr', False),

                # işlem masrafları ne kadar
                # ('match', {'regex':r'^islem masraf[a-z]*( ne)*( kadar)* .$'}, 'history_tr', 'price_rates_tr', {}),

                # askeri tutar ne kadar oduyecedim
                # ('match', {'regex':r'^as[gk][ae]ri tutar( ne kadar){0,1} od[eiuy][a-z]* .$'}, 'history_tr', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['askeri']}),

                # Kartımla alışveriş yapabilir miyim
                # ('match', {'regex':r'^kart[a-z]* alisveris[a-z]* yap[a-z]* *[a-z]* .$'}, 'online_shopping_tr', 'spendadvice_tr', {'_TARGET_SVP_': ['alisveris']}),

                # İnternet bankacılığı
                # ('match', {'regex':r'^internet[a-z]* bank[a-z]* .$'}, 'online_shopping_tr', 'internet_sube_giris', False),
                
                # turkcell finans
                # ('match', {'regex':r'^turkcell[a-z]* finans[a-z]* .$'}, 'inform#transfer_money_tr', 'inform#bill_payment_tr', False),

                # bana para verebilir misin biraz
                # ('match', {'regex':r'^bana para ver[a-z]*( m[iu][a-z]*){0,1}( biraz[a-z]*){0,1} .$'}, 'bad_habit_tr', 'cash_advance_tr', False),

                # taksitlendirilmiş kredi kartı borcumu ödemek istiyorum
                # ('match', {'regex':r'^taksit[a-z]* kredi karti bor[a-z]* ode[a-z]*( [a-z]*){0,1} .$'}, 'installment_closure_tr', 'credit_card_payment_tr', False),

                # kredi taksitlerimi nasıl öderim
                # ('match', {'regex':r'^kredi[a-z]* taksit[a-z]*( nasil){0,1} ode[a-z]* .$'}, 'credit_info_tr', 'credit_payment_tr', False),

                # Yeni eft hesabını nasıl kaydedebilirim
                # ('match', {'regex':r'^([a-z]* ){0,1}eft hesa[a-z]*( nasil){0,1} kayde[a-z]* .$'}, 'delete_eft_tr', 'eft_identify_tr', False),

                # döviz oranları
                # ('match', {'regex':r'^doviz[a-z]* oran[a-z]* .$'}, 'term_deposit_calculation_tr', 'foreign_currency_tr', {'_TARGET_AMOUNT_TR_': ['doviz']}),

                # sen salaksin 
                # ('findall', {'regex':r'\bsalak'}, 'good_comment_tr', 'bad_comment_tr', False),

                # Fatura ödeme menüsünü açar mısın
                # ('findall', {'regex':r'fatura.*menu'}, 'billpayment_orders_tr', 'bill_payment_tr', False),

                # Kredi kartından para aktarma 
                # ('match', {'regex':r'^kredi[a-z]* kart[a-z]* para[a-z]* aktar[a-z]* .$'}, 'baskabanka_kkr_odeme', 'cash_advance_tr', False),

                # en son yaptığım havale tarihi
                # ('match', {'regex':r'^en[a-z]* son[a-z]* yap[a-z]* havale[a-z]* tarih[a-z]* .$'}, 'transfer_info_tr', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z','endDate': '2021-02-14T23:59:59Z','tokens': 'DEFAULT GENERATED'}],'_TARGET_SVP_': ['havale']}),
                # ('match', {'regex':r'^en[a-z]* son[a-z]* yap[a-z]* eft[a-z]* tarih[a-z]* .$'}, 'transfer_info_tr', 'txnlist_tr', {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z','endDate': '2021-02-14T23:59:59Z','tokens': 'DEFAULT GENERATED'}],'_TARGET_SVP_': ['eft']}),

                # Kredi kartı askeriyesi ne kadar 
                # ('match', {'regex':r'^kredi[a-z]* kart[a-z]* as[kg][aei].* .$'}, 'extract_tr', 'credit_card_payment_tr', {'_PAYMENT_TYPE_TR_': ['askeri']}),

                # faturayi nereden odicem
                # ('match', {'regex':r'^fatura[a-z]* ner[a-z]* od[a-z]* .$'}, 'txnlist_tr', 'bill_payment_tr', {}),
                # Genel Hesap Kapatma islemi
                # ('match', {'regex':r'genel[a-z]* hesa[a-z]* kapa[a-z]*'}, 'ek_hesap_kapama', 'generel_account_closure_tr', False),
                # kart aidatı kesmişsiniz
                # ('match', {'regex':r'kart[a-z]* aidat[a-z]* kes[a-z]*mis[a-z]*'}, 'card_fee_tr', 'card_fee_refund_tr', False),
                # Altın nasıl alınır
                # ('2nd_score', {'confidence':0.3}, 'open_gold_account_tr', 'gold_buy_sale_tr', False),
                # kart puanım, kart puanlarım, kartimdaki puanlarim, kartımdaki puanlar
                # ('match', {'regex':r'^kart[a-z]* pua[a-z]* .$'}, 'my_earnings_tr', 'credit_card_tr', False),
                # Su faturası ödeme talimatı
                # ('findall', {r'talimat(?!(s[iı]z))'}, 'bill_payment_tr', 'billpayment_orders_tr', {}),
                

            ]
            self.message_mapping_func(message, mapping_config)

            intent = message.get(INTENT)
            if False:
                pass
            # elif intent['name'] == 'txnlist_tr': 
            #     if bool(re.findall(r'\b(gel|gir|maas|hareket|kazan)', message.text)): # gönderilen
            #         pass
            #     else:
            #         if bool(re.findall(r'\d ay', message.text)):
            #             message.set(INTENT, {'name': 'history_tr', 'confidence': 0.998})
            #         elif bool(re.findall(r'toplam', message.text)):
            #             message.set(INTENT, {'name': 'history_tr', 'confidence': 0.998})

            elif intent['name'] == 'inform#ek_hesap_bilgileri':
                message.set(INTENT, {'name': 'ek_hesap_bilgileri', 'confidence': intent['confidence']})

            elif bool(re.findall(r'\d{12,28}', message.text.replace(" ",""))): # TR030012300678101141727000 # tr\d{8,28}
                message.set(INTENT, {'name': 'transfer_to_undefined_account_tr', 'confidence': 0.998})
                message.set("entities", {})
                message.set("mcm_entities", {})

        elif processor == "isyatirim":
            pass



        elif processor == "tokens_to_output":
            tokens = message.get('tokens')
            if tokens[-1].text == '__CLS__':
                tokens = tokens[:-1]
            if tokens[-1].text == '.':
                tokens = tokens[:-1]
                
            message.set('_tokens', message.get('tokens'), add_to_output=True)

        elif processor == "clear_entities":
            message.set(ENTITIES, [], add_to_output=False)




        elif processor == "duckling_amount_of_money_with_kurus":

            entities = message.get(ENTITIES, [])

            for e in entities:
                if 'Duckling' in e['extractor'] and e['entity'] == 'amount-of-money':
                    if e['value'] % 1 != 0:
                        e['entity'] = 'amount-of-money-with-kurus'

        elif processor == "duckling_remove_amount_of_money_without_unit":

            entities = message.get(ENTITIES, [])
            
            entities = [e for e in entities 
                        if not ( 'Duckling' in e['extractor'] and 
                                 e['entity'] in ['amount-of-money', 'amount-of-money-with-kurus'] and 
                                 'unit' not in e['additional_info']      )
                        ]
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
            if message.text in self.t_dict:
                print(message.text)
                print('  > ' + {self.t_dict[message.text]}  )
                print('  > ' + message.get(INTENT)  ) 
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
        dl = self.subclass_delimiter
        intent = message.get(INTENT)
        if ['name'] in intent:
            if dl in intent['name']:
                message.set(INTENT, {'name': intent['name'].rsplit(dl, 1)[0], 'confidence': intent['confidence']})
    

class EntityManager(Component):

    defaults = {
        "priority_config": {},
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
    def split_rasa_entity_merge(entities):
        entities_updated = entities

        if False:
            other_entities = [e for e in entities_updated if "DIET" not in e['extractor'] ]
            model_entities = [e for e in entities_updated if "DIET" in e['extractor'] ]
            model_entities = sorted(model_entities, key=lambda x: x['start'])

            splitted_model_entities = []
            for e in model_entities:
                if e['entity'].startswith('B-'):
                    if e['entity'] == 'B-currency':
                        e['value'].split()

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
        entities_updated = EntityManager.split_rasa_entity_merge(entities_updated)
        entities_updated = EntityManager.merge_BI_entities(message, entities_updated)
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

        # message.set("raw_entities", entities, add_to_output=True)
        # entities = self.map_entities(intent['name'], entities)
        # message.set("entities", entities, add_to_output=True)
        
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
            if output['_BUY_TR_'] == []:
                if output['_REF_AMOUNT_TR_'] != []:
                    temppostprocessing = output['_TARGET_AMOUNT_TR_']
                    output['_TARGET_AMOUNT_TR_'] = output['_REF_AMOUNT_TR_']
                    output['_REF_AMOUNT_TR_'] = temppostprocessing

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
            if target_entity is not False:
                message.set("entities", target_entities)


        if message_intent != source_intent:
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
            matched = self.message_mapping_base(message, intent, intent_ranking[1], *m) # mode, rule, source_intent, target_intent, target_entities
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
        
            intent = message.get(INTENT)
            entities = message.get(ENTITIES, [])

            if False:
                pass

            # elif intent['name'] == 'my_earnings_tr': # kart puanım, kart puanlarım, kartimdaki puanlarim, kartımdaki puanlar
            #     if re.match(r'^kart[a-z]* pua[a-z]* .$', message.text):
            #         message.set(INTENT, {'name': 'credit_card_tr', 'confidence': 0.998})

            elif 'transfer_to_undefined_account_tr' in intent['name']:

                if intent['name'] == 'transfer_to_undefined_account_tr_diger' and re.match(r'^diger[a-z]* gelir[a-z]* .$', message.text): 
                    # diger gelir
                    message.set(INTENT, {'name': 'txnlist_tr', 'confidence': 0.998})
                else:
                    message.set(INTENT, {'name': 'transfer_to_undefined_account_tr', 'confidence': intent['confidence']})


            elif intent['name'] == 'account_tr':
                # Kredi kartı askeriyesi ne kadar
                if re.match(r'^vades[a-z]* euro[a-z]* hes[a-z]* sat[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_AMOUNT_TR_': ['euro'], '_SELL_TR_': ['sat']})
                    message.set("mcm_entities", {'_TARGET_AMOUNT_TR_': ['euro'], '_SELL_TR_': ['sat']})
                elif re.match(r'^vades[a-z]* euro[a-z]* hes[a-z]* al[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_AMOUNT_TR_': ['euro'], '_BUY_TR_': ['al']})
                    message.set("mcm_entities", {'_TARGET_AMOUNT_TR_': ['euro'], '_BUY_TR_': ['al']})
                elif re.match(r'^vade[a-z]* dolar[a-z]* hes[a-z]* sat[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_AMOUNT_TR_': ['dolar'], '_SELL_TR_': ['sat']})
                    message.set("mcm_entities", {'_TARGET_AMOUNT_TR_': ['dolar'], '_SELL_TR_': ['sat']})
                elif re.match(r'^vade[a-z]* dolar[a-z]* hes[a-z]* al[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']})
                    message.set("mcm_entities", {'_TARGET_AMOUNT_TR_': ['dolar'], '_BUY_TR_': ['al']})
                elif re.match(r'^euro[a-z]* ne[a-z]*kadar[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_AMOUNT_TR_': ['euro']})
                    message.set("mcm_entities", {'_TARGET_AMOUNT_TR_': ['euro']})


            elif intent['name'] == 'credit_card_tr': 
                # 2018 maxipuan
                if '2018' in message.text and bool(re.findall(r'puan', message.text)):
                    message.set(INTENT, {'name': 'my_earnings_tr', 'confidence': 0.998})
                    message.set("entities", {})
                    message.set("mcm_entities", {})

                # Kredi kartı askeriyesi ne kadar
                elif bool(re.findall(r'askeri', message.text)):
                    message.set(INTENT, {'name': 'credit_card_payment_tr', 'confidence': 0.998})
                    message.set("entities", {'_PAYMENT_TYPE_TR_': ['askeri']})
                    message.set("mcm_entities", {'_PAYMENT_TYPE_TR_': ['askeri']})

            # elif intent['name'] == 'bill_payment_tr': # Su faturası ödeme talimatı
            #     if re.findall(r'talimat(?!(s[iı]z))', message.text):
            #         message.set(INTENT, {'name': 'billpayment_orders_tr', 'confidence': 0.998})
            #         message.set("entities", {})

            elif intent['name'] == 'debt_config_tr': 
                # borç versene
                if re.match(r'^borc ver[a-z]*( misin)* .$', message.text):
                    message.set(INTENT, {'name': 'cash_advance_tr', 'confidence': 0.998})

            elif intent['name'] == 'card_info_tr': 
                # Kart bilgilerim çalındı 	
                if re.match(r'^kart bilgi[a-z]* cal[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'lost_stolen_card_tr', 'confidence': 0.998})

            elif intent['name'] == '2a2a4': 
                # kredi başvuru ayrıntıları 	
                if re.match(r'^kredi[a-z]* basvuru[a-z]* ayrinti[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'credit_application_track_tr', 'confidence': 0.998})

            elif intent['name'] == '6a6a13': 
                # eft masrafı
                if re.match(r'^eft masraf[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'price_rates_tr', 'confidence': 0.998})

            elif intent['name'] == 'history_tr': 
                # işlem masrafları ne kadar
                if re.match(r'^islem masraf[a-z]*( ne)*( kadar)* .$', message.text):
                    message.set(INTENT, {'name': 'price_rates_tr', 'confidence': 0.998})
                
                # askeri tutar ne kadar oduyecedim
                elif re.match(r'^as[gk][ae]ri tutar( ne kadar){0,1} od[eiuy][a-z]* .$', message.text): 
                    message.set(INTENT, {'name': 'credit_card_payment_tr', 'confidence': 0.998})
                    message.set("entities", {'_PAYMENT_TYPE_TR_': ['askeri']})
                    message.set("mcm_entities", {'_PAYMENT_TYPE_TR_': ['askeri']})

            elif intent['name'] == 'online_shopping_tr': 
                # Kartımla alışveriş yapabilir miyim
                if re.match(r'^kart[a-z]* alisveris[a-z]* yap[a-z]* *[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'spendadvice_tr', 'confidence': 0.998})
                    message.set("entities", {'_TARGET_SVP_': ['alisveris']})
                    message.set("mcm_entities", {'_TARGET_SVP_': ['alisveris']})
                # İnternet bankacılığı
                elif re.match(r'^internet[a-z]* bank[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'internet_sube_giris', 'confidence': 0.998})

            elif intent['name'] == 'inform#transfer_money_tr': 
                # turkcell finans
                if re.match(r'^turkcell[a-z]* finans[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'inform#bill_payment_tr', 'confidence': 0.998})

            elif intent['name'] == 'bad_habit_tr': 
                # bana para verebilir misin biraz
                if re.match(r'^bana para ver[a-z]*( m[iu][a-z]*){0,1}( biraz[a-z]*){0,1} .$', message.text):
                    message.set(INTENT, {'name': 'cash_advance_tr', 'confidence': 0.998})

            elif intent['name'] == 'installment_closure_tr': 
                # taksitlendirilmiş kredi kartı borcumu ödemek istiyorum
                if re.match(r'^taksit[a-z]* kredi karti bor[a-z]* ode[a-z]*( [a-z]*){0,1} .$', message.text):
                    message.set(INTENT, {'name': 'credit_card_payment_tr', 'confidence': 0.998})

            elif intent['name'] == 'credit_info_tr': 
                # kredi taksitlerimi nasıl öderim
                if re.match(r'^kredi[a-z]* taksit[a-z]*( nasil){0,1} ode[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'credit_payment_tr', 'confidence': 0.998})

            elif intent['name'] == 'delete_eft_tr': 
                # Yeni eft hesabını nasıl kaydedebilirim
                if re.match(r'^([a-z]* ){0,1}eft hesa[a-z]*( nasil){0,1} kayde[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'eft_identify_tr', 'confidence': 0.998})

            elif intent['name'] == 'term_deposit_calculation_tr': 
                # döviz oranları
                if re.match(r'^doviz[a-z]* oran[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'foreign_currency_tr', 'confidence': 0.998})


            elif intent['name'] == 'good_comment_tr': 
                # sen salaksin
                if bool(re.findall(r'\bsalak', message.text)):
                    message.set(INTENT, {'name': 'bad_comment_tr', 'confidence': 0.998})


            elif intent['name'] == 'billpayment_orders_tr': 
                # Fatura ödeme menüsünü açar mısın
                if bool(re.findall(r'fatura.*menu', message.text)):
                    message.set(INTENT, {'name': 'bill_payment_tr', 'confidence': 0.998})

            elif intent['name'] == 'baskabanka_kkr_odeme': 
                # Kredi kartından para aktarma
                if re.match(r'^kredi[a-z]* kart[a-z]* para[a-z]* aktar[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'cash_advance_tr', 'confidence': 0.998})

            elif intent['name'] == 'transfer_info_tr': 
                # en son yaptığım havale tarihi
                if re.match(r'^en[a-z]* son[a-z]* yap[a-z]* havale[a-z]* tarih[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'txnlist_tr', 'confidence': 0.998})
                    message.set("entities", {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z',
                                                'endDate': '2021-02-14T23:59:59Z',
                                                'tokens': 'DEFAULT GENERATED'}],
                                            '_TARGET_SVP_': ['havale']})
                    message.set("mcm_entities", {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z',
                                                'endDate': '2021-02-14T23:59:59Z',
                                                'tokens': 'DEFAULT GENERATED'}],
                                            '_TARGET_SVP_': ['havale']})
                elif re.match(r'^en[a-z]* son[a-z]* yap[a-z]* eft[a-z]* tarih[a-z]* .$', message.text):
                    message.set(INTENT, {'name': 'txnlist_tr', 'confidence': 0.998})
                    message.set("entities", {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z',
                                                'endDate': '2021-02-14T23:59:59Z',
                                                'tokens': 'DEFAULT GENERATED'}],
                                            '_TARGET_SVP_': ['eft']})
                    message.set("mcm_entities", {'_DATE_': [{'startDate': '2020-10-14T00:00:00Z',
                                                'endDate': '2021-02-14T23:59:59Z',
                                                'tokens': 'DEFAULT GENERATED'}],
                                            '_TARGET_SVP_': ['eft']})


            elif intent['name'] == 'extract_tr': 
                # Kredi kartı askeriyesi ne kadar
                if re.match(r'^kredi[a-z]* kart[a-z]* as[kg][aei].* .$', message.text):
                    message.set(INTENT, {'name': 'credit_card_payment_tr', 'confidence': 0.998})
                    message.set("entities", {'_PAYMENT_TYPE_TR_': ['askeri']})
                    message.set("mcm_entities", {'_PAYMENT_TYPE_TR_': ['askeri']})


            elif intent['name'] == 'txnlist_tr': 
                if bool(re.findall(r'\b(gel|gir|maas|hareket|kazan)', message.text)):
                    pass
                else:
                    if bool(re.findall(r'\d ay', message.text)):
                        message.set(INTENT, {'name': 'history_tr', 'confidence': 0.998})
                    elif bool(re.findall(r'toplam', message.text)):
                        message.set(INTENT, {'name': 'history_tr', 'confidence': 0.998})


            # faturayi nereden odicem
            #     if re.match(r'^fatura[a-z]* ner[a-z]* od[a-z]* .$', message.text):
            #         message.set(INTENT, {'name': 'bill_payment_tr', 'confidence': 0.998})
            #         message.set("entities", {})
                    
            # elif intent['name'] == 'ek_hesap_kapama': # Genel Hesap Kapatma islemi
            #     if re.match(r'genel[a-z]* hesa[a-z]* kapa[a-z]*', message.text):
            #         message.set(INTENT, {'name': 'generel_account_closure_tr', 'confidence': 0.998})

            # elif intent['name'] == 'card_fee_tr': # kart aidatı kesmişsiniz
            #     if re.match(r'kart[a-z]* aidat[a-z]* kes[a-z]*mis[a-z]*', message.text):
            #         message.set(INTENT, {'name': 'card_fee_refund_tr', 'confidence': 0.998})

            # elif intent['name'] == 'open_gold_account_tr': # Altın nasıl alınır
            #     intent_ranking = message.get('intent_ranking')
            #     c1 = intent_ranking[0]
            #     c2 = intent_ranking[1]
            #     if c2['name'] == 'gold_buy_sale_tr' and c2['confidence'] > 0.3 :
            #         message.set(INTENT, {'name': 'gold_buy_sale_tr', 'confidence': 0.998})

            # elif intent['name'] == 'inform#history_tr- Flo giyim': # inform#history_tr- Flo giyim
            #     message.set(INTENT, {'name': 'inform#history_tr', 'confidence': intent['confidence']})

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
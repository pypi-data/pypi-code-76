
import pyspace_resources
datasets_path = pyspace_resources.__path__[0] + '/datasets'


import pandas as pd
import numpy as np

import re
import string

from pyspace.re.refunctions import convert_list_to_regex
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer


def load_names(first_char_upper=False, mode='merged'):
    names_path = datasets_path + '/turkish/names'

    blacklist = ['gonder', 'tamam', 'ana', 'istanbul', 'izmir', 'dolar', 'bakiye', 'altin', 'gediz', 'var', 'varlik', 'kart', 'par', 'biten', 'bite', 'pek', 'kar', 'yatir', 'yatır', 'son', 'hadi', ]

    names_male = pd.read_csv(f'{names_path}/male_name_tally', delimiter=' ', header=None)
    names_female = pd.read_csv(f'{names_path}/female_name_tally', delimiter=' ', header=None)
    names_last = pd.read_csv(f'{names_path}/lastname_tally.csv', delimiter=' ', header=None)

    def prune_v1(names_df):
        
        names_df = names_df.dropna()
        
        names_df = names_df[names_df[0].apply(lambda x: set([str(i) for i in range(10)]).intersection(set(x)) == set() )]    
        names_df = names_df[names_df[0].apply(lambda x: set(string.punctuation).intersection(set(x)) == set() )]
        
        names_df['len'] = names_df[0].apply(lambda x: len(x))
        
        names_df = names_df[names_df['len'] != 1]
        names_df = names_df[names_df['len'] != 2]
        
        return names_df
        
    names_male = prune_v1(names_male)
    names_female = prune_v1(names_female)
    names_last = prune_v1(names_last)

    names_male = list(names_male[names_male[1]>400][0].values)
    names_female = list(names_female[names_female[1]>400][0].values)
    names_last = list(names_last[names_last[1]>400][0].values) + ['PEKALP']

    names_male = [n for n in names_male if xNormalizer.tr_normalize(n).lower() not in blacklist]
    names_female = [n for n in names_female if xNormalizer.tr_normalize(n).lower() not in blacklist]
    names_last = [n for n in names_last if xNormalizer.tr_normalize(n).lower() not in blacklist]

    if first_char_upper:
        names_male = [t[0] + t[1:].lower() for t in names_male]
        names_female = [t[0] + t[1:].lower() for t in names_female]
        names_last = [t[0] + t[1:].lower() for t in names_last]

    names_synonyms = list(set(names_female + names_male + names_last ))

    if mode == 'merged':
        return names_synonyms
    elif mode == 'merged_regex':
        return convert_list_to_regex(names_synonyms)
    elif mode == 'separate':
        return names_male, names_female, names_last
    elif mode == 'separate_regex':
        return convert_list_to_regex(names_male), convert_list_to_regex(names_female), convert_list_to_regex(names_last)
    else:
        return "INVALID MODE"
    
def load_branches(mode='list'):
    bankingbranch_path = datasets_path + '/turkish/banking/branch'
    bankingbranch_filename = bankingbranch_path + '/isbanksube.txt'

    sube = pd.read_csv(bankingbranch_filename, header=None, )
    sube.columns = ['raw']

    sube['code'], sube['raw'] = zip(*sube['raw'].map(lambda x: x.strip().split(' ',1) ) )
    sube['sube'], sube['city'] = zip(*sube['raw'].map(lambda x: x.split('/') if '/' in x else ('/'+x).split('/') ))
    sube['code'] = sube['code'].apply(lambda x: x.strip())
    sube['sube'] = sube['sube'].apply(lambda x: x.strip())
    sube['city'] = sube['city'].apply(lambda x: x.strip())

    subelist = sube[sube['sube'].apply(lambda x: len(x.split()) == 1)]['sube'].values
    multiword_subelist = list(sube[sube['sube'].apply(lambda x: len(x.split()) != 1 and x != '')]['sube'].values)
    _temp_dashed = [item for sublist in [d.split('-') for d in subelist if '-' in d] for item in sublist] 
    subelist = [d for d in subelist if '-' not in d]
    subelist = subelist + _temp_dashed
    sube_namelist = list(set(subelist))
    sube_sehirlist = list(set(sube['city'].apply(lambda x: x.replace("Kurumsal","").replace("Adalet Sarayı","").replace("Özel Bankacılık","").replace("Havalimanı","").replace("Ticari","").replace("OSB","").strip()).values )) + ['OSB']
    sube_codelist = list(set(sube['code'].values))

    sube_synonyms = list(set(sube_sehirlist + sube_namelist + multiword_subelist + sube_codelist)) + ['Cevizlibağ']


    if mode == 'list':
        return sube_synonyms
    elif mode == 'regex':
        return convert_list_to_regex(sube_synonyms) 
    else:
        return "INVALID MODE"

def load_billing_agencies(mode='list'):
    
    bill_agency_path = datasets_path + '/turkish/bill_agency'
    bill_agency_filename = bill_agency_path + '/bill_agency.txt'

    agencies = pd.read_csv(bill_agency_filename, header=None, )
    agencies.columns = ['raw']

    agencies['raw'] = agencies['raw'].apply(lambda x: x.strip())

    agencies = list(agencies.drop_duplicates()['raw'].values)

    if mode == 'list':
        return agencies
    elif mode == 'regex':
        return convert_list_to_regex(agencies)
    else:
        return "INVALID MODE"



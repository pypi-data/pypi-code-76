parameters = [[{'GroupName': 'DLT-support'}, {'GroupName': 'PoweruserAssumers'}, {'GroupName': 'test_group'}],
   [{'PolicyName':'+.'}],[{'HitlersBunker':'500'}]
              ]
from collections import ChainMap
from itertools import product

poo = [dict(ChainMap(*a)) for a in list(product(*parameters))]

print('ok')
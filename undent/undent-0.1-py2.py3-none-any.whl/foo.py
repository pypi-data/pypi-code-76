#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from api import *
from icecream import ic


print(undent('''
    Once upon a time, there was a
    little girl named Goldilocks.
      ''', strip=False))


s = f'''
            Could not find property.

            Did you run this tool via "pipenv run ..." instead of
            bin/verify-installation.sh? Use the latter to set up the production
            or development environment variables appropriately.


            Did you run this tool via "pipenv run ..." instead of
            a


'''

p = '''            Did you run this tool via "pipenv run ..." instead of
            bin/verify-installation.sh? Use the latter to set up the production
            or development environment variables appropriately.'''


#print(p)
#print(unwrap(p))

#ic(splitIntoParagraphs(s))

#ic(undent(s))
#print(s)
#print()
#print(undent(s))
#print()
#print(undent(s, 45))

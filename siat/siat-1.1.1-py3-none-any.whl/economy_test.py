# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.economy import *

cn=compare_economy(['China','USA'],'GNP','1995-1-1','2020-1-1')
cn=compare_economy(['China','Japan'],'GNP','1995-1-1','2010-1-1')
cn=compare_economy(['USA','Japan'],'GNP','1995-1-1','2010-1-1')


df=pmi_china('2020-1-5','2020-10-1')

df=pmi_china('2019-1-5','2020-10-31')


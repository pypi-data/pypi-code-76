import os
import platform
import sys
from pathlib import Path
PATH_TO_SETTINGS=''
for dirpath, dirnames, files in os.walk('./'):
    if dirpath[len('./'):].count(os.sep) < 1:
        if 'settings.py' in files:
            PATH_TO_SETTINGS = dirpath[2:] + '.settings'
if platform.system()=='Windows':
    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent) + '\\')
else:
    sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent.parent) + '/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", PATH_TO_SETTINGS)
import django

django.setup()

from django.conf import settings

LOAD_BALANCER = settings.LOAD_BALANCER
DATABASES = settings.DATABASES
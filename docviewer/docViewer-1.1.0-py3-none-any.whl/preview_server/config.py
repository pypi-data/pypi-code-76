import os
from docViewer.config import CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

CACHE_ROOT = CONFIG['CACHE_ROOT']
DOC_ROOT = CONFIG.get('DOC_ROOT', os.path.dirname(os.path.curdir))

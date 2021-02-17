from vytools.config import ITEMS, CONFIG
from vytools.ui import server
from vytools._actions import build, run, info, _scan
from vytools.utils import get_repository_paths

def scan(contextpaths=None):
  (success, items) = _scan(contextpaths=contextpaths)
  ITEMS.clear()
  ITEMS.update(items)
  CONFIG.set('items',[i for i in items]) # Always write items?
  return success

__version__ = "0.0.39"

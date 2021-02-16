"""
Keys of special search space definition entries.
"""

from ..run.special_entries import UNSEARCHABLE_ENTRIES as UNSEARCHABLE_RUN_ENTRIES

HYPEROPT_KEY = '__hp__'
TUPLE_KEY = '__tuple__'

def unsearchable_run_entry(obj):
    return any(unsearchable_entry in obj 
               for unsearchable_entry in UNSEARCHABLE_RUN_ENTRIES)

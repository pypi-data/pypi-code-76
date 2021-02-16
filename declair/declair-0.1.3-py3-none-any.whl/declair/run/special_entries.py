"""
Keys of special run definition entries.
"""

ENV_KEY = '__env__'
CALL_KEY = '__call__'
TYPE_KEY = '__type__'
VAR_KEY = '__var__'
VAR_INSTANCE_KEY = '__var_instance__'

# These dictionary entries should be left as they are while performing search,
# without recursing deeper into their values.
UNSEARCHABLE_ENTRIES = [
    ENV_KEY
]

# These dictionary entries should be checked for sources to store in Sacred
ENTRIES_WITH_SOURCES = [
    CALL_KEY,
    TYPE_KEY
]

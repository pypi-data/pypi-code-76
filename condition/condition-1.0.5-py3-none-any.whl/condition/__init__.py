from ._condition import (
    Field,
    FieldList,
    FieldCondition,
    CompositeCondition,
    Condition,
    And,
    Or,
    Operator,
    get_test_df,
)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

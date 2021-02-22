'''_1540.py

BearingLoadCaseResultsForPst
'''


from mastapy.bearings import _1541
from mastapy._internal.python_net import python_net_import

_BEARING_LOAD_CASE_RESULTS_FOR_PST = python_net_import('SMT.MastaAPI.Bearings', 'BearingLoadCaseResultsForPst')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCaseResultsForPst',)


class BearingLoadCaseResultsForPst(_1541.BearingLoadCaseResultsLightweight):
    '''BearingLoadCaseResultsForPst

    This is a mastapy class.
    '''

    TYPE = _BEARING_LOAD_CASE_RESULTS_FOR_PST

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingLoadCaseResultsForPst.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

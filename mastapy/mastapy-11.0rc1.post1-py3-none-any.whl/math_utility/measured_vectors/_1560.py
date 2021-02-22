'''_1560.py

ForceResults
'''


from mastapy.math_utility.measured_vectors import _1558
from mastapy._internal.python_net import python_net_import

_FORCE_RESULTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'ForceResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ForceResults',)


class ForceResults(_1558.AbstractForceAndDisplacementResults):
    '''ForceResults

    This is a mastapy class.
    '''

    TYPE = _FORCE_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ForceResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

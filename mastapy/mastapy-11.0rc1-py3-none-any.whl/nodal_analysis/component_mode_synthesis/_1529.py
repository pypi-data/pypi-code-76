'''_1529.py

StaticCMSResults
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _1528
from mastapy._internal.python_net import python_net_import

_STATIC_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'StaticCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticCMSResults',)


class StaticCMSResults(_1528.RealCMSResults):
    '''StaticCMSResults

    This is a mastapy class.
    '''

    TYPE = _STATIC_CMS_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StaticCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_stress(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateStress

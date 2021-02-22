'''_202.py

StaticCMSResults
'''


from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _201
from mastapy._internal.python_net import python_net_import

_STATIC_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'StaticCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticCMSResults',)


class StaticCMSResults(_201.RealCMSResults):
    '''StaticCMSResults

    This is a mastapy class.
    '''

    TYPE = _STATIC_CMS_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StaticCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def calculate_stress(self):
        ''' 'CalculateStress' is the original name of this method.'''

        self.wrapped.CalculateStress()

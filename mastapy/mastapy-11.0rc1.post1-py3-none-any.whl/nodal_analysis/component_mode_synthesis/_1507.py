'''_1507.py

RealCMSResults
'''


from mastapy.nodal_analysis.component_mode_synthesis import _1503
from mastapy._internal.python_net import python_net_import

_REAL_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'RealCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RealCMSResults',)


class RealCMSResults(_1503.CMSResults):
    '''RealCMSResults

    This is a mastapy class.
    '''

    TYPE = _REAL_CMS_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RealCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

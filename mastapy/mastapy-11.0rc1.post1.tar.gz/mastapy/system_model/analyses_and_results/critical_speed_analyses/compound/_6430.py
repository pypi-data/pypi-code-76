'''_6430.py

VirtualComponentCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6385
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'VirtualComponentCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundCriticalSpeedAnalysis',)


class VirtualComponentCompoundCriticalSpeedAnalysis(_6385.MountableComponentCompoundCriticalSpeedAnalysis):
    '''VirtualComponentCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

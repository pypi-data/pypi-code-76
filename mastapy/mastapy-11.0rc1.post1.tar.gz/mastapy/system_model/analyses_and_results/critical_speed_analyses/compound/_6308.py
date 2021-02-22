'''_6308.py

AbstractAssemblyCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6387
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AbstractAssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundCriticalSpeedAnalysis',)


class AbstractAssemblyCompoundCriticalSpeedAnalysis(_6387.PartCompoundCriticalSpeedAnalysis):
    '''AbstractAssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

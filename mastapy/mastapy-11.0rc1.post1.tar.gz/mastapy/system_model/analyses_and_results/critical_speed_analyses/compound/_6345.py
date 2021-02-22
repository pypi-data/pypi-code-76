'''_6345.py

CouplingCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6406
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CouplingCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundCriticalSpeedAnalysis',)


class CouplingCompoundCriticalSpeedAnalysis(_6406.SpecialisedAssemblyCompoundCriticalSpeedAnalysis):
    '''CouplingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

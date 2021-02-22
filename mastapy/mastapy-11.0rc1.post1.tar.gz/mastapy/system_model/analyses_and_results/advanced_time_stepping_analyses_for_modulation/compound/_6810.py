'''_6810.py

CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6848
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation',)


class CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation(_6848.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

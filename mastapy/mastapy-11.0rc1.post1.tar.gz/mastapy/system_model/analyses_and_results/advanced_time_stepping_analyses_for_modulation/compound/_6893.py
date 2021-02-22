'''_6893.py

VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6848
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation',)


class VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation(_6848.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

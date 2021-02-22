'''_6812.py

CVTCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6781
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'CVTCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundAdvancedTimeSteppingAnalysisForModulation',)


class CVTCompoundAdvancedTimeSteppingAnalysisForModulation(_6781.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''CVTCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

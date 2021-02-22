'''_6811.py

CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6780
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation',)


class CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(_6780.BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

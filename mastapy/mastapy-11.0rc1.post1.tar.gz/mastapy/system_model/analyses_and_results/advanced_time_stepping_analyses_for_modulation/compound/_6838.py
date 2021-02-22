'''_6838.py

KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6804
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation',)


class KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(_6804.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

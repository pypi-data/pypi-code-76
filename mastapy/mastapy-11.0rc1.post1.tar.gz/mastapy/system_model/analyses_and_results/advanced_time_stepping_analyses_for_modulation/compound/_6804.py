'''_6804.py

ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6830
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(_6830.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation))
        return value

'''_4727.py

StraightBevelGearMeshCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4597
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4635
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'StraightBevelGearMeshCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundModalAnalysisAtASpeed',)


class StraightBevelGearMeshCompoundModalAnalysisAtASpeed(_4635.BevelGearMeshCompoundModalAnalysisAtASpeed):
    '''StraightBevelGearMeshCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4597.StraightBevelGearMeshModalAnalysisAtASpeed]':
        '''List[StraightBevelGearMeshModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4597.StraightBevelGearMeshModalAnalysisAtASpeed))
        return value

    @property
    def connection_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4597.StraightBevelGearMeshModalAnalysisAtASpeed]':
        '''List[StraightBevelGearMeshModalAnalysisAtASpeed]: 'ConnectionModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtASpeedLoadCases, constructor.new(_4597.StraightBevelGearMeshModalAnalysisAtASpeed))
        return value

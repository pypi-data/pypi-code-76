'''_4628.py

BeltDriveCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2247, _2257
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4499
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4716
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'BeltDriveCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundModalAnalysisAtASpeed',)


class BeltDriveCompoundModalAnalysisAtASpeed(_4716.SpecialisedAssemblyCompoundModalAnalysisAtASpeed):
    '''BeltDriveCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2247.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.BeltDrive.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2247.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.BeltDrive.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BeltDrive. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4499.BeltDriveModalAnalysisAtASpeed]':
        '''List[BeltDriveModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4499.BeltDriveModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4499.BeltDriveModalAnalysisAtASpeed]':
        '''List[BeltDriveModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4499.BeltDriveModalAnalysisAtASpeed))
        return value

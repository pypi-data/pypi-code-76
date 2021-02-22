'''_3921.py

BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3919, _3920, _3926
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3797
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses',)


class BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses(_3926.BevelGearSetCompoundModalAnalysesAtStiffnesses):
    '''BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2114.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3919.BevelDifferentialGearCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_3919.BevelDifferentialGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3920.BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_3920.BevelDifferentialGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3797.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3797.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3797.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3797.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value

'''_4023.py

BevelDifferentialGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2098
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6109
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4022, _4021, _4028
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'BevelDifferentialGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetModalAnalysesAtSpeeds',)


class BevelDifferentialGearSetModalAnalysesAtSpeeds(_4028.BevelGearSetModalAnalysesAtSpeeds):
    '''BevelDifferentialGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2098.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2098.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6109.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6109.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_modal_analyses_at_speeds(self) -> 'List[_4022.BevelDifferentialGearModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearModalAnalysesAtSpeeds]: 'BevelDifferentialGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsModalAnalysesAtSpeeds, constructor.new(_4022.BevelDifferentialGearModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_meshes_modal_analyses_at_speeds(self) -> 'List[_4021.BevelDifferentialGearMeshModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearMeshModalAnalysesAtSpeeds]: 'BevelDifferentialMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesModalAnalysesAtSpeeds, constructor.new(_4021.BevelDifferentialGearMeshModalAnalysesAtSpeeds))
        return value

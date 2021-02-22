'''_6549.py

KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2212
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6547, _6548, _6543
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase',)


class KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase(_6543.KlingelnbergCycloPalloidConicalGearSetLoadCase):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2212.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2212.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def gears(self) -> 'List[_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_load_case(self) -> 'List[_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsLoadCase, constructor.new(_6547.KlingelnbergCycloPalloidSpiralBevelGearLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_load_case(self) -> 'List[_6548.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesLoadCase, constructor.new(_6548.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase))
        return value

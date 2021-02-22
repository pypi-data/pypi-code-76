'''_5310.py

BevelDifferentialGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2098
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6109
from mastapy.system_model.analyses_and_results.system_deflections import _2261
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5308, _5309, _5315
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BevelDifferentialGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetGearWhineAnalysis',)


class BevelDifferentialGearSetGearWhineAnalysis(_5315.BevelGearSetGearWhineAnalysis):
    '''BevelDifferentialGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2261.BevelDifferentialGearSetSystemDeflection':
        '''BevelDifferentialGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2261.BevelDifferentialGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5308.BevelDifferentialGearGearWhineAnalysis]':
        '''List[BevelDifferentialGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5308.BevelDifferentialGearGearWhineAnalysis))
        return value

    @property
    def bevel_differential_gears_gear_whine_analysis(self) -> 'List[_5308.BevelDifferentialGearGearWhineAnalysis]':
        '''List[BevelDifferentialGearGearWhineAnalysis]: 'BevelDifferentialGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsGearWhineAnalysis, constructor.new(_5308.BevelDifferentialGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5309.BevelDifferentialGearMeshGearWhineAnalysis]':
        '''List[BevelDifferentialGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5309.BevelDifferentialGearMeshGearWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_gear_whine_analysis(self) -> 'List[_5309.BevelDifferentialGearMeshGearWhineAnalysis]':
        '''List[BevelDifferentialGearMeshGearWhineAnalysis]: 'BevelDifferentialMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesGearWhineAnalysis, constructor.new(_5309.BevelDifferentialGearMeshGearWhineAnalysis))
        return value

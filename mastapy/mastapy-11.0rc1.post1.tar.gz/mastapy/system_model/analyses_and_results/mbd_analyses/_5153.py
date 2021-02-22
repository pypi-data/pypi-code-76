'''_5153.py

StraightBevelGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2219
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6595
from mastapy.system_model.analyses_and_results.mbd_analyses import _5152, _5151, _5049
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetMultibodyDynamicsAnalysis',)


class StraightBevelGearSetMultibodyDynamicsAnalysis(_5049.BevelGearSetMultibodyDynamicsAnalysis):
    '''StraightBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2219.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2219.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6595.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6595.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5152.StraightBevelGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5152.StraightBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5152.StraightBevelGearMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearMultibodyDynamicsAnalysis]: 'StraightBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsMultibodyDynamicsAnalysis, constructor.new(_5152.StraightBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5151.StraightBevelGearMeshMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshMultibodyDynamicsAnalysis]: 'StraightBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesMultibodyDynamicsAnalysis, constructor.new(_5151.StraightBevelGearMeshMultibodyDynamicsAnalysis))
        return value

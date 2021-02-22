'''_5171.py

WormGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6616
from mastapy.system_model.analyses_and_results.mbd_analyses import _5170, _5169, _5093
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetMultibodyDynamicsAnalysis',)


class WormGearSetMultibodyDynamicsAnalysis(_5093.GearSetMultibodyDynamicsAnalysis):
    '''WormGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2223.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6616.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6616.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5170.WormGearMultibodyDynamicsAnalysis]':
        '''List[WormGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5170.WormGearMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_gears_multibody_dynamics_analysis(self) -> 'List[_5170.WormGearMultibodyDynamicsAnalysis]':
        '''List[WormGearMultibodyDynamicsAnalysis]: 'WormGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsMultibodyDynamicsAnalysis, constructor.new(_5170.WormGearMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_meshes_multibody_dynamics_analysis(self) -> 'List[_5169.WormGearMeshMultibodyDynamicsAnalysis]':
        '''List[WormGearMeshMultibodyDynamicsAnalysis]: 'WormMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesMultibodyDynamicsAnalysis, constructor.new(_5169.WormGearMeshMultibodyDynamicsAnalysis))
        return value

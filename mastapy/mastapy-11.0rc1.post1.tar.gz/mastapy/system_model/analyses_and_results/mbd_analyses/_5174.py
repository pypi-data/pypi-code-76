'''_5174.py

ZerolBevelGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6619
from mastapy.system_model.analyses_and_results.mbd_analyses import _5173, _5172, _5049
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetMultibodyDynamicsAnalysis',)


class ZerolBevelGearSetMultibodyDynamicsAnalysis(_5049.BevelGearSetMultibodyDynamicsAnalysis):
    '''ZerolBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6619.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6619.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5173.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5173.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5173.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'ZerolBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsMultibodyDynamicsAnalysis, constructor.new(_5173.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5172.ZerolBevelGearMeshMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshMultibodyDynamicsAnalysis]: 'ZerolBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesMultibodyDynamicsAnalysis, constructor.new(_5172.ZerolBevelGearMeshMultibodyDynamicsAnalysis))
        return value

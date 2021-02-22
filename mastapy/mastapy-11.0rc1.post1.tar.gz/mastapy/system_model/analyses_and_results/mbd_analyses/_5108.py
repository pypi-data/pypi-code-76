'''_5108.py

KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6546
from mastapy.system_model.analyses_and_results.mbd_analyses import _5107, _5106, _5105
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis(_5105.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6546.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6546.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5107.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5107.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_multibody_dynamics_analysis(self) -> 'List[_5107.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsMultibodyDynamicsAnalysis, constructor.new(_5107.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_multibody_dynamics_analysis(self) -> 'List[_5106.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesMultibodyDynamicsAnalysis, constructor.new(_5106.KlingelnbergCycloPalloidHypoidGearMeshMultibodyDynamicsAnalysis))
        return value

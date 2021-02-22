'''_5063.py

ConceptGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2193
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6474
from mastapy.system_model.analyses_and_results.mbd_analyses import _5062, _5061, _5093
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ConceptGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetMultibodyDynamicsAnalysis',)


class ConceptGearSetMultibodyDynamicsAnalysis(_5093.GearSetMultibodyDynamicsAnalysis):
    '''ConceptGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2193.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6474.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6474.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5062.ConceptGearMultibodyDynamicsAnalysis]':
        '''List[ConceptGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5062.ConceptGearMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_gears_multibody_dynamics_analysis(self) -> 'List[_5062.ConceptGearMultibodyDynamicsAnalysis]':
        '''List[ConceptGearMultibodyDynamicsAnalysis]: 'ConceptGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsMultibodyDynamicsAnalysis, constructor.new(_5062.ConceptGearMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_meshes_multibody_dynamics_analysis(self) -> 'List[_5061.ConceptGearMeshMultibodyDynamicsAnalysis]':
        '''List[ConceptGearMeshMultibodyDynamicsAnalysis]: 'ConceptMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesMultibodyDynamicsAnalysis, constructor.new(_5061.ConceptGearMeshMultibodyDynamicsAnalysis))
        return value

'''_5079.py

CylindricalGearMeshMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy.system_model.analyses_and_results.static_loads import _6494
from mastapy.system_model.analyses_and_results.mbd_analyses import _5090
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CylindricalGearMeshMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMultibodyDynamicsAnalysis',)


class CylindricalGearMeshMultibodyDynamicsAnalysis(_5090.GearMeshMultibodyDynamicsAnalysis):
    '''CylindricalGearMeshMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_stress_gear_a_left_flank(self) -> 'float':
        '''float: 'ContactStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearALeftFlank

    @property
    def contact_stress_gear_b_left_flank(self) -> 'float':
        '''float: 'ContactStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearBLeftFlank

    @property
    def contact_stress_gear_a_right_flank(self) -> 'float':
        '''float: 'ContactStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearARightFlank

    @property
    def contact_stress_gear_b_right_flank(self) -> 'float':
        '''float: 'ContactStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearBRightFlank

    @property
    def tooth_root_stress_gear_a_left_flank(self) -> 'float':
        '''float: 'ToothRootStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearALeftFlank

    @property
    def tooth_root_stress_gear_b_left_flank(self) -> 'float':
        '''float: 'ToothRootStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearBLeftFlank

    @property
    def tooth_root_stress_gear_a_right_flank(self) -> 'float':
        '''float: 'ToothRootStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearARightFlank

    @property
    def tooth_root_stress_gear_b_right_flank(self) -> 'float':
        '''float: 'ToothRootStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearBRightFlank

    @property
    def connection_design(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6494.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6494.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshMultibodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshMultibodyDynamicsAnalysis))
        return value

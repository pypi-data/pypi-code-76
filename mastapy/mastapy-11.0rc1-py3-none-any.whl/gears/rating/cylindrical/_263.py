'''_263.py

CylindricalMeshDutyCycleRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import _254
from mastapy.gears.rating import _164
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalMeshDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshDutyCycleRating',)


class CylindricalMeshDutyCycleRating(_164.MeshDutyCycleRating):
    '''CylindricalMeshDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESH_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def micropitting_safety_factor(self) -> 'float':
        '''float: 'MicropittingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingSafetyFactor

    @property
    def scuffing_safety_factor_flash_temperature_method(self) -> 'float':
        '''float: 'ScuffingSafetyFactorFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorFlashTemperatureMethod

    @property
    def scuffing_safety_factor_integral_temperature_method(self) -> 'float':
        '''float: 'ScuffingSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorIntegralTemperatureMethod

    @property
    def scuffing_load_safety_factor_integral_temperature_method(self) -> 'float':
        '''float: 'ScuffingLoadSafetyFactorIntegralTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingLoadSafetyFactorIntegralTemperatureMethod

    @property
    def permanent_deformation_safety_factor_step_1(self) -> 'float':
        '''float: 'PermanentDeformationSafetyFactorStep1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PermanentDeformationSafetyFactorStep1

    @property
    def permanent_deformation_safety_factor_step_2(self) -> 'float':
        '''float: 'PermanentDeformationSafetyFactorStep2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PermanentDeformationSafetyFactorStep2

    @property
    def maximum_radial_separating_load(self) -> 'float':
        '''float: 'MaximumRadialSeparatingLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumRadialSeparatingLoad

    @property
    def maximum_nominal_axial_force(self) -> 'float':
        '''float: 'MaximumNominalAxialForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNominalAxialForce

    @property
    def maximum_nominal_tangential_load(self) -> 'float':
        '''float: 'MaximumNominalTangentialLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNominalTangentialLoad

    @property
    def highest_torque_load_case(self) -> '_254.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'HighestTorqueLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_254.CylindricalGearMeshRating)(self.wrapped.HighestTorqueLoadCase) if self.wrapped.HighestTorqueLoadCase else None

    @property
    def cylindrical_mesh_ratings(self) -> 'List[_254.CylindricalGearMeshRating]':
        '''List[CylindricalGearMeshRating]: 'CylindricalMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshRatings, constructor.new(_254.CylindricalGearMeshRating))
        return value

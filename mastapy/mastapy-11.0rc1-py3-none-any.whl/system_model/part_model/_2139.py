'''_2139.py

OilSeal
'''


from mastapy.materials.efficiency import _263
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results import _1660
from mastapy.system_model.part_model import _2121
from mastapy._internal.python_net import python_net_import

_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSeal',)


class OilSeal(_2121.Connector):
    '''OilSeal

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSeal.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def oil_seal_material(self) -> '_263.OilSealMaterialType':
        '''OilSealMaterialType: 'OilSealMaterial' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OilSealMaterial)
        return constructor.new(_263.OilSealMaterialType)(value) if value else None

    @oil_seal_material.setter
    def oil_seal_material(self, value: '_263.OilSealMaterialType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealMaterial = value

    @property
    def oil_seal_characteristic_life(self) -> 'float':
        '''float: 'OilSealCharacteristicLife' is the original name of this property.'''

        return self.wrapped.OilSealCharacteristicLife

    @oil_seal_characteristic_life.setter
    def oil_seal_characteristic_life(self, value: 'float'):
        self.wrapped.OilSealCharacteristicLife = float(value) if value else 0.0

    @property
    def oil_seal_mean_time_before_failure(self) -> 'float':
        '''float: 'OilSealMeanTimeBeforeFailure' is the original name of this property.'''

        return self.wrapped.OilSealMeanTimeBeforeFailure

    @oil_seal_mean_time_before_failure.setter
    def oil_seal_mean_time_before_failure(self, value: 'float'):
        self.wrapped.OilSealMeanTimeBeforeFailure = float(value) if value else 0.0

    @property
    def slope_of_linear_equation_defining_the_effect_of_temperature(self) -> 'float':
        '''float: 'SlopeOfLinearEquationDefiningTheEffectOfTemperature' is the original name of this property.'''

        return self.wrapped.SlopeOfLinearEquationDefiningTheEffectOfTemperature

    @slope_of_linear_equation_defining_the_effect_of_temperature.setter
    def slope_of_linear_equation_defining_the_effect_of_temperature(self, value: 'float'):
        self.wrapped.SlopeOfLinearEquationDefiningTheEffectOfTemperature = float(value) if value else 0.0

    @property
    def intercept_of_linear_equation_defining_the_effect_of_temperature(self) -> 'float':
        '''float: 'InterceptOfLinearEquationDefiningTheEffectOfTemperature' is the original name of this property.'''

        return self.wrapped.InterceptOfLinearEquationDefiningTheEffectOfTemperature

    @intercept_of_linear_equation_defining_the_effect_of_temperature.setter
    def intercept_of_linear_equation_defining_the_effect_of_temperature(self, value: 'float'):
        self.wrapped.InterceptOfLinearEquationDefiningTheEffectOfTemperature = float(value) if value else 0.0

    @property
    def oil_seal_frictional_torque_coefficient(self) -> 'float':
        '''float: 'OilSealFrictionalTorqueCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OilSealFrictionalTorqueCoefficient

    @property
    def width(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Width' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Width) if self.wrapped.Width else None

    @width.setter
    def width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Width = value

    @property
    def oil_seal_orientation(self) -> '_1660.Orientations':
        '''Orientations: 'OilSealOrientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OilSealOrientation)
        return constructor.new(_1660.Orientations)(value) if value else None

    @oil_seal_orientation.setter
    def oil_seal_orientation(self, value: '_1660.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealOrientation = value

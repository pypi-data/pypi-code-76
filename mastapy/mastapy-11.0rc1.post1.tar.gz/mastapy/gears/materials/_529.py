'''_529.py

AGMACylindricalGearMaterial
'''


from mastapy.materials import _207, _208, _209
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.materials import _537
from mastapy._internal.python_net import python_net_import

_AGMA_CYLINDRICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'AGMACylindricalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMACylindricalGearMaterial',)


class AGMACylindricalGearMaterial(_537.CylindricalGearMaterial):
    '''AGMACylindricalGearMaterial

    This is a mastapy class.
    '''

    TYPE = _AGMA_CYLINDRICAL_GEAR_MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMACylindricalGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def material_application(self) -> '_207.AGMAMaterialApplications':
        '''AGMAMaterialApplications: 'MaterialApplication' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MaterialApplication)
        return constructor.new(_207.AGMAMaterialApplications)(value) if value else None

    @material_application.setter
    def material_application(self, value: '_207.AGMAMaterialApplications'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialApplication = value

    @property
    def stress_cycle_factor_at_1e10_cycles_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesContact' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.StressCycleFactorAt1E10CyclesContact) if self.wrapped.StressCycleFactorAt1E10CyclesContact else None

    @stress_cycle_factor_at_1e10_cycles_contact.setter
    def stress_cycle_factor_at_1e10_cycles_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.StressCycleFactorAt1E10CyclesContact = value

    @property
    def stress_cycle_factor_at_1e10_cycles_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesBending' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.StressCycleFactorAt1E10CyclesBending) if self.wrapped.StressCycleFactorAt1E10CyclesBending else None

    @stress_cycle_factor_at_1e10_cycles_bending.setter
    def stress_cycle_factor_at_1e10_cycles_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.StressCycleFactorAt1E10CyclesBending = value

    @property
    def material_class(self) -> '_208.AGMAMaterialClasses':
        '''AGMAMaterialClasses: 'MaterialClass' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MaterialClass)
        return constructor.new(_208.AGMAMaterialClasses)(value) if value else None

    @material_class.setter
    def material_class(self, value: '_208.AGMAMaterialClasses'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialClass = value

    @property
    def grade(self) -> '_209.AGMAMaterialGrade':
        '''AGMAMaterialGrade: 'Grade' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Grade)
        return constructor.new(_209.AGMAMaterialGrade)(value) if value else None

    @grade.setter
    def grade(self, value: '_209.AGMAMaterialGrade'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Grade = value

    @property
    def allowable_stress_number_bending(self) -> 'float':
        '''float: 'AllowableStressNumberBending' is the original name of this property.'''

        return self.wrapped.AllowableStressNumberBending

    @allowable_stress_number_bending.setter
    def allowable_stress_number_bending(self, value: 'float'):
        self.wrapped.AllowableStressNumberBending = float(value) if value else 0.0

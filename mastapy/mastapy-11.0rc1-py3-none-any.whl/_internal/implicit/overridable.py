'''overridable.py

Implementations of 'Overridable' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from enum import Enum
from typing import Generic, TypeVar

from mastapy._internal import (
    mixins, constructor, enum_with_selected_value_runtime, conversion
)
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _216
from mastapy.gears import (
    _294, _279, _282, _297
)
from mastapy.bearings.bearing_designs.rolling import _1858, _1842, _1840
from mastapy.nodal_analysis.dev_tools_analyses import _171
from mastapy.nodal_analysis.fe_export_utility import _147
from mastapy.system_model.fe import _2075
from mastapy.materials.efficiency import _255, _257
from mastapy.gears.rating.cylindrical.iso6336 import _464

_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'Overridable')


__docformat__ = 'restructuredtext en'
__all__ = (
    'Overridable_float', 'Overridable_int',
    'Overridable_CylindricalGearRatingMethods', 'Overridable_ISOToleranceStandard',
    'Overridable_CoefficientOfFrictionCalculationMethod', 'Overridable_T',
    'Overridable_WidthSeries', 'Overridable_HeightSeries',
    'Overridable_DiameterSeries', 'Overridable_bool',
    'Overridable_RigidCouplingType', 'Overridable_BoundaryConditionType',
    'Overridable_NodeSelectionDepthOption', 'Overridable_BearingEfficiencyRatingMethod',
    'Overridable_ContactRatioRequirements', 'Overridable_MicroGeometryModel',
    'Overridable_HelicalGearMicroGeometryOption', 'Overridable_EfficiencyRatingMethod'
)


T = TypeVar('T')


class Overridable_float(float, mixins.OverridableMixin):
    '''Overridable_float

    A specific implementation of 'Overridable' for 'float' types.
    '''

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'Overridable_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.Value) if instance_to_wrap.Value else 0.0

    def __init__(self, instance_to_wrap: 'Overridable_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'float':
        '''float: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'float':
        '''float: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue


class Overridable_int(int, mixins.OverridableMixin):
    '''Overridable_int

    A specific implementation of 'Overridable' for 'int' types.
    '''

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'Overridable_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.Value) if instance_to_wrap.Value else 0

    def __init__(self, instance_to_wrap: 'Overridable_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def value(self) -> 'int':
        '''int: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'int':
        '''int: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'int':
        '''int: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue


class Overridable_CylindricalGearRatingMethods(mixins.OverridableMixin, Enum):
    '''Overridable_CylindricalGearRatingMethods

    A specific implementation of 'Overridable' for 'CylindricalGearRatingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_216.CylindricalGearRatingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _216.CylindricalGearRatingMethods.type_()

    @property
    def value(self) -> '_216.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_216.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_216.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_ISOToleranceStandard(mixins.OverridableMixin, Enum):
    '''Overridable_ISOToleranceStandard

    A specific implementation of 'Overridable' for 'ISOToleranceStandard' types.
    '''

    __hash__ = None
    __qualname__ = 'ISOToleranceStandard'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_294.ISOToleranceStandard.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _294.ISOToleranceStandard.type_()

    @property
    def value(self) -> '_294.ISOToleranceStandard':
        '''ISOToleranceStandard: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_294.ISOToleranceStandard':
        '''ISOToleranceStandard: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_294.ISOToleranceStandard':
        '''ISOToleranceStandard: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_CoefficientOfFrictionCalculationMethod(mixins.OverridableMixin, Enum):
    '''Overridable_CoefficientOfFrictionCalculationMethod

    A specific implementation of 'Overridable' for 'CoefficientOfFrictionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'CoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_279.CoefficientOfFrictionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _279.CoefficientOfFrictionCalculationMethod.type_()

    @property
    def value(self) -> '_279.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_279.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_279.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_T(Generic[T], mixins.OverridableMixin):
    '''Overridable_T

    A specific implementation of 'Overridable' for 'T' types.
    '''

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'Overridable_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def value(self) -> 'T':
        '''T: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.enclosing.Value) if self.enclosing.Value else None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'T':
        '''T: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.enclosing.OverrideValue) if self.enclosing.OverrideValue else None

    @property
    def calculated_value(self) -> 'T':
        '''T: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.enclosing.CalculatedValue) if self.enclosing.CalculatedValue else None


class Overridable_WidthSeries(mixins.OverridableMixin, Enum):
    '''Overridable_WidthSeries

    A specific implementation of 'Overridable' for 'WidthSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'WidthSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_1858.WidthSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1858.WidthSeries.type_()

    @property
    def value(self) -> '_1858.WidthSeries':
        '''WidthSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1858.WidthSeries':
        '''WidthSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1858.WidthSeries':
        '''WidthSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_HeightSeries(mixins.OverridableMixin, Enum):
    '''Overridable_HeightSeries

    A specific implementation of 'Overridable' for 'HeightSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'HeightSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_1842.HeightSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1842.HeightSeries.type_()

    @property
    def value(self) -> '_1842.HeightSeries':
        '''HeightSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1842.HeightSeries':
        '''HeightSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1842.HeightSeries':
        '''HeightSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_DiameterSeries(mixins.OverridableMixin, Enum):
    '''Overridable_DiameterSeries

    A specific implementation of 'Overridable' for 'DiameterSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'DiameterSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_1840.DiameterSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1840.DiameterSeries.type_()

    @property
    def value(self) -> '_1840.DiameterSeries':
        '''DiameterSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1840.DiameterSeries':
        '''DiameterSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1840.DiameterSeries':
        '''DiameterSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_bool(mixins.OverridableMixin):
    '''Overridable_bool

    A specific implementation of 'Overridable' for 'bool' types.
    '''

    __hash__ = None
    __qualname__ = 'bool'

    def __new__(cls, instance_to_wrap: 'Overridable_bool.TYPE'):
        return bool.__new__(cls, instance_to_wrap.Value) if instance_to_wrap.Value else False

    def __init__(self, instance_to_wrap: 'Overridable_bool.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'bool':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return bool

    @property
    def value(self) -> 'bool':
        '''bool: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'bool':
        '''bool: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'bool':
        '''bool: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue

    def __bool__(self):
        return self.value


class Overridable_RigidCouplingType(mixins.OverridableMixin, Enum):
    '''Overridable_RigidCouplingType

    A specific implementation of 'Overridable' for 'RigidCouplingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidCouplingType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_171.RigidCouplingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _171.RigidCouplingType.type_()

    @property
    def value(self) -> '_171.RigidCouplingType':
        '''RigidCouplingType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_171.RigidCouplingType':
        '''RigidCouplingType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_171.RigidCouplingType':
        '''RigidCouplingType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_BoundaryConditionType(mixins.OverridableMixin, Enum):
    '''Overridable_BoundaryConditionType

    A specific implementation of 'Overridable' for 'BoundaryConditionType' types.
    '''

    __hash__ = None
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_147.BoundaryConditionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _147.BoundaryConditionType.type_()

    @property
    def value(self) -> '_147.BoundaryConditionType':
        '''BoundaryConditionType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_147.BoundaryConditionType':
        '''BoundaryConditionType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_147.BoundaryConditionType':
        '''BoundaryConditionType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_NodeSelectionDepthOption(mixins.OverridableMixin, Enum):
    '''Overridable_NodeSelectionDepthOption

    A specific implementation of 'Overridable' for 'NodeSelectionDepthOption' types.
    '''

    __hash__ = None
    __qualname__ = 'NodeSelectionDepthOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_2075.NodeSelectionDepthOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2075.NodeSelectionDepthOption.type_()

    @property
    def value(self) -> '_2075.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_2075.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_2075.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_BearingEfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    '''Overridable_BearingEfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'BearingEfficiencyRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingEfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_255.BearingEfficiencyRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _255.BearingEfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_255.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_255.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_255.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_ContactRatioRequirements(mixins.OverridableMixin, Enum):
    '''Overridable_ContactRatioRequirements

    A specific implementation of 'Overridable' for 'ContactRatioRequirements' types.
    '''

    __hash__ = None
    __qualname__ = 'ContactRatioRequirements'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_282.ContactRatioRequirements.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _282.ContactRatioRequirements.type_()

    @property
    def value(self) -> '_282.ContactRatioRequirements':
        '''ContactRatioRequirements: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_282.ContactRatioRequirements':
        '''ContactRatioRequirements: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_282.ContactRatioRequirements':
        '''ContactRatioRequirements: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_MicroGeometryModel(mixins.OverridableMixin, Enum):
    '''Overridable_MicroGeometryModel

    A specific implementation of 'Overridable' for 'MicroGeometryModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_297.MicroGeometryModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _297.MicroGeometryModel.type_()

    @property
    def value(self) -> '_297.MicroGeometryModel':
        '''MicroGeometryModel: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_297.MicroGeometryModel':
        '''MicroGeometryModel: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_297.MicroGeometryModel':
        '''MicroGeometryModel: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_HelicalGearMicroGeometryOption(mixins.OverridableMixin, Enum):
    '''Overridable_HelicalGearMicroGeometryOption

    A specific implementation of 'Overridable' for 'HelicalGearMicroGeometryOption' types.
    '''

    __hash__ = None
    __qualname__ = 'HelicalGearMicroGeometryOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_464.HelicalGearMicroGeometryOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _464.HelicalGearMicroGeometryOption.type_()

    @property
    def value(self) -> '_464.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_464.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_464.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_EfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    '''Overridable_EfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'EfficiencyRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'EfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> '_257.EfficiencyRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _257.EfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_257.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_257.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_257.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

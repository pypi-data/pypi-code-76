'''_774.py

CylindricalGearDefaults
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import _801
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _878
from mastapy.gears.manufacturing.cylindrical.cutters import _522
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _496
from mastapy.utility import _1157

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_DEFAULTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDefaults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDefaults',)


class CylindricalGearDefaults(_1157.PerMachineSettings):
    '''CylindricalGearDefaults

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DEFAULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDefaults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def chamfer_angle(self) -> 'float':
        '''float: 'ChamferAngle' is the original name of this property.'''

        return self.wrapped.ChamferAngle

    @chamfer_angle.setter
    def chamfer_angle(self, value: 'float'):
        self.wrapped.ChamferAngle = float(value) if value else 0.0

    @property
    def diameter_chamfer_height(self) -> 'float':
        '''float: 'DiameterChamferHeight' is the original name of this property.'''

        return self.wrapped.DiameterChamferHeight

    @diameter_chamfer_height.setter
    def diameter_chamfer_height(self, value: 'float'):
        self.wrapped.DiameterChamferHeight = float(value) if value else 0.0

    @property
    def fillet_roughness(self) -> 'float':
        '''float: 'FilletRoughness' is the original name of this property.'''

        return self.wrapped.FilletRoughness

    @fillet_roughness.setter
    def fillet_roughness(self, value: 'float'):
        self.wrapped.FilletRoughness = float(value) if value else 0.0

    @property
    def flank_roughness(self) -> 'float':
        '''float: 'FlankRoughness' is the original name of this property.'''

        return self.wrapped.FlankRoughness

    @flank_roughness.setter
    def flank_roughness(self, value: 'float'):
        self.wrapped.FlankRoughness = float(value) if value else 0.0

    @property
    def iso_quality_grade(self) -> 'int':
        '''int: 'ISOQualityGrade' is the original name of this property.'''

        return self.wrapped.ISOQualityGrade

    @iso_quality_grade.setter
    def iso_quality_grade(self, value: 'int'):
        self.wrapped.ISOQualityGrade = int(value) if value else 0

    @property
    def gear_fit_system(self) -> '_801.GearFitSystems':
        '''GearFitSystems: 'GearFitSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearFitSystem)
        return constructor.new(_801.GearFitSystems)(value) if value else None

    @gear_fit_system.setter
    def gear_fit_system(self, value: '_801.GearFitSystems'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFitSystem = value

    @property
    def iso_material(self) -> 'str':
        '''str: 'ISOMaterial' is the original name of this property.'''

        return self.wrapped.ISOMaterial.SelectedItemName

    @iso_material.setter
    def iso_material(self, value: 'str'):
        self.wrapped.ISOMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def agma_material(self) -> 'str':
        '''str: 'AGMAMaterial' is the original name of this property.'''

        return self.wrapped.AGMAMaterial.SelectedItemName

    @agma_material.setter
    def agma_material(self, value: 'str'):
        self.wrapped.AGMAMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def use_toleranced_value_for_finish_stock(self) -> 'bool':
        '''bool: 'UseTolerancedValueForFinishStock' is the original name of this property.'''

        return self.wrapped.UseTolerancedValueForFinishStock

    @use_toleranced_value_for_finish_stock.setter
    def use_toleranced_value_for_finish_stock(self, value: 'bool'):
        self.wrapped.UseTolerancedValueForFinishStock = bool(value) if value else False

    @property
    def system_of_fits_defaults(self) -> '_878.DIN3967SystemOfGearFits':
        '''DIN3967SystemOfGearFits: 'SystemOfFitsDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_878.DIN3967SystemOfGearFits)(self.wrapped.SystemOfFitsDefaults) if self.wrapped.SystemOfFitsDefaults else None

    @property
    def rough_cutter_creation_settings(self) -> '_522.RoughCutterCreationSettings':
        '''RoughCutterCreationSettings: 'RoughCutterCreationSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_522.RoughCutterCreationSettings)(self.wrapped.RoughCutterCreationSettings) if self.wrapped.RoughCutterCreationSettings else None

    @property
    def rough_manufacturing_process_controls(self) -> '_496.ManufacturingProcessControls':
        '''ManufacturingProcessControls: 'RoughManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_496.ManufacturingProcessControls)(self.wrapped.RoughManufacturingProcessControls) if self.wrapped.RoughManufacturingProcessControls else None

    @property
    def finish_manufacturing_process_controls(self) -> '_496.ManufacturingProcessControls':
        '''ManufacturingProcessControls: 'FinishManufacturingProcessControls' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_496.ManufacturingProcessControls)(self.wrapped.FinishManufacturingProcessControls) if self.wrapped.FinishManufacturingProcessControls else None

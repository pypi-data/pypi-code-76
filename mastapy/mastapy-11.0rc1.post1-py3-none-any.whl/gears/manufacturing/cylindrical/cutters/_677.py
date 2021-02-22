'''_677.py

CylindricalGearRealCutterDesign
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.scripting import _7192
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import (
    _687, _688, _689, _690,
    _691, _692, _694
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _668, _670
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearRealCutterDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRealCutterDesign',)


class CylindricalGearRealCutterDesign(_670.CylindricalGearAbstractCutterDesign):
    '''CylindricalGearRealCutterDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearRealCutterDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def has_tolerances(self) -> 'bool':
        '''bool: 'HasTolerances' is the original name of this property.'''

        return self.wrapped.HasTolerances

    @has_tolerances.setter
    def has_tolerances(self, value: 'bool'):
        self.wrapped.HasTolerances = bool(value) if value else False

    @property
    def normal_pitch(self) -> 'float':
        '''float: 'NormalPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPitch

    @property
    def normal_base_pitch(self) -> 'float':
        '''float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalBasePitch

    @property
    def normal_pressure_angle_constant_base_pitch(self) -> 'float':
        '''float: 'NormalPressureAngleConstantBasePitch' is the original name of this property.'''

        return self.wrapped.NormalPressureAngleConstantBasePitch

    @normal_pressure_angle_constant_base_pitch.setter
    def normal_pressure_angle_constant_base_pitch(self, value: 'float'):
        self.wrapped.NormalPressureAngleConstantBasePitch = float(value) if value else 0.0

    @property
    def number_of_points_for_reporting_fillet_shape(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingFilletShape' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingFilletShape) if self.wrapped.NumberOfPointsForReportingFilletShape else None

    @number_of_points_for_reporting_fillet_shape.setter
    def number_of_points_for_reporting_fillet_shape(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfPointsForReportingFilletShape = value

    @property
    def nominal_cutter_drawing(self) -> '_7192.SMTBitmap':
        '''SMTBitmap: 'NominalCutterDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7192.SMTBitmap)(self.wrapped.NominalCutterDrawing) if self.wrapped.NominalCutterDrawing else None

    @property
    def number_of_points_for_reporting_main_blade_shape(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingMainBladeShape' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingMainBladeShape) if self.wrapped.NumberOfPointsForReportingMainBladeShape else None

    @number_of_points_for_reporting_main_blade_shape.setter
    def number_of_points_for_reporting_main_blade_shape(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfPointsForReportingMainBladeShape = value

    @property
    def specify_custom_blade_shape(self) -> 'bool':
        '''bool: 'SpecifyCustomBladeShape' is the original name of this property.'''

        return self.wrapped.SpecifyCustomBladeShape

    @specify_custom_blade_shape.setter
    def specify_custom_blade_shape(self, value: 'bool'):
        self.wrapped.SpecifyCustomBladeShape = bool(value) if value else False

    @property
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CutterAndGearNormalBasePitchComparisonTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance) if self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance else None

    @cutter_and_gear_normal_base_pitch_comparison_tolerance.setter
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance = value

    @property
    def nominal_cutter_shape(self) -> '_687.CutterShapeDefinition':
        '''CutterShapeDefinition: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _687.CutterShapeDefinition.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CutterShapeDefinition. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_formed_wheel_grinder_tangible(self) -> '_688.CylindricalGearFormedWheelGrinderTangible':
        '''CylindricalGearFormedWheelGrinderTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _688.CylindricalGearFormedWheelGrinderTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearFormedWheelGrinderTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_hob_shape(self) -> '_689.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _689.CylindricalGearHobShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearHobShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_shaper_tangible(self) -> '_690.CylindricalGearShaperTangible':
        '''CylindricalGearShaperTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _690.CylindricalGearShaperTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearShaperTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_shaver_tangible(self) -> '_691.CylindricalGearShaverTangible':
        '''CylindricalGearShaverTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _691.CylindricalGearShaverTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearShaverTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_692.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _692.CylindricalGearWormGrinderShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_rack_shape(self) -> '_694.RackShape':
        '''RackShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _694.RackShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to RackShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NominalCutterShape.__class__)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def customised_cutting_edge_profile(self) -> '_668.CustomisableEdgeProfile':
        '''CustomisableEdgeProfile: 'CustomisedCuttingEdgeProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_668.CustomisableEdgeProfile)(self.wrapped.CustomisedCuttingEdgeProfile) if self.wrapped.CustomisedCuttingEdgeProfile else None

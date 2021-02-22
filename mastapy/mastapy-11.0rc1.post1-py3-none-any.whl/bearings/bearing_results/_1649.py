'''_1649.py

LoadedBearingResults
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1660
from mastapy.math_utility.measured_vectors import _1327
from mastapy.bearings.bearing_designs import (
    _1820, _1821, _1822, _1823,
    _1824
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1825, _1826, _1827, _1828,
    _1829, _1830, _1832, _1837,
    _1838, _1839, _1841, _1843,
    _1844, _1845, _1846, _1849,
    _1850, _1852, _1853, _1854,
    _1855, _1856, _1857
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1870, _1872, _1874, _1876,
    _1877, _1878
)
from mastapy.bearings.bearing_designs.concept import _1880, _1881, _1882
from mastapy.bearings.bearing_results.rolling import _1762
from mastapy.bearings import _1582
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingResults',)


class LoadedBearingResults(_1582.BearingLoadCaseResultsLightweight):
    '''LoadedBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_of_gravity_from_z_axis(self) -> 'float':
        '''float: 'AngleOfGravityFromZAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngleOfGravityFromZAxis

    @property
    def signed_relative_speed(self) -> 'float':
        '''float: 'SignedRelativeSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedRelativeSpeed

    @property
    def relative_speed(self) -> 'float':
        '''float: 'RelativeSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeSpeed

    @property
    def inner_race_speed(self) -> 'float':
        '''float: 'InnerRaceSpeed' is the original name of this property.'''

        return self.wrapped.InnerRaceSpeed

    @inner_race_speed.setter
    def inner_race_speed(self, value: 'float'):
        self.wrapped.InnerRaceSpeed = float(value) if value else 0.0

    @property
    def outer_race_speed(self) -> 'float':
        '''float: 'OuterRaceSpeed' is the original name of this property.'''

        return self.wrapped.OuterRaceSpeed

    @outer_race_speed.setter
    def outer_race_speed(self, value: 'float'):
        self.wrapped.OuterRaceSpeed = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.'''

        return self.wrapped.Duration

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def orientation(self) -> '_1660.Orientations':
        '''Orientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_1660.Orientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_1660.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def specified_radial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedRadialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedRadialInternalClearance

    @specified_radial_internal_clearance.setter
    def specified_radial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedRadialInternalClearance = float(value) if value else 0.0

    @property
    def specified_axial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedAxialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedAxialInternalClearance

    @specified_axial_internal_clearance.setter
    def specified_axial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedAxialInternalClearance = float(value) if value else 0.0

    @property
    def axial_displacement_preload(self) -> 'float':
        '''float: 'AxialDisplacementPreload' is the original name of this property.'''

        return self.wrapped.AxialDisplacementPreload

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'float'):
        self.wrapped.AxialDisplacementPreload = float(value) if value else 0.0

    @property
    def force_results_are_overridden(self) -> 'bool':
        '''bool: 'ForceResultsAreOverridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceResultsAreOverridden

    @property
    def relative_axial_displacement(self) -> 'float':
        '''float: 'RelativeAxialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeAxialDisplacement

    @property
    def relative_radial_displacement(self) -> 'float':
        '''float: 'RelativeRadialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeRadialDisplacement

    @property
    def force_on_inner_race(self) -> '_1327.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceOnInnerRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1327.VectorWithLinearAndAngularComponents)(self.wrapped.ForceOnInnerRace) if self.wrapped.ForceOnInnerRace else None

    @property
    def bearing(self) -> '_1820.BearingDesign':
        '''BearingDesign: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1820.BearingDesign.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BearingDesign. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_detailed_bearing(self) -> '_1821.DetailedBearing':
        '''DetailedBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1821.DetailedBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DetailedBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_dummy_rolling_bearing(self) -> '_1822.DummyRollingBearing':
        '''DummyRollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1822.DummyRollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DummyRollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_linear_bearing(self) -> '_1823.LinearBearing':
        '''LinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1823.LinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to LinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_non_linear_bearing(self) -> '_1824.NonLinearBearing':
        '''NonLinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1824.NonLinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonLinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_angular_contact_ball_bearing(self) -> '_1825.AngularContactBallBearing':
        '''AngularContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1825.AngularContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_angular_contact_thrust_ball_bearing(self) -> '_1826.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1826.AngularContactThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_asymmetric_spherical_roller_bearing(self) -> '_1827.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1827.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1828.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1828.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_axial_thrust_needle_roller_bearing(self) -> '_1829.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1829.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_ball_bearing(self) -> '_1830.BallBearing':
        '''BallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1830.BallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_barrel_roller_bearing(self) -> '_1832.BarrelRollerBearing':
        '''BarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1832.BarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_crossed_roller_bearing(self) -> '_1837.CrossedRollerBearing':
        '''CrossedRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1837.CrossedRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to CrossedRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_cylindrical_roller_bearing(self) -> '_1838.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1838.CylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_deep_groove_ball_bearing(self) -> '_1839.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1839.DeepGrooveBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_four_point_contact_ball_bearing(self) -> '_1841.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1841.FourPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_multi_point_contact_ball_bearing(self) -> '_1843.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1843.MultiPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_needle_roller_bearing(self) -> '_1844.NeedleRollerBearing':
        '''NeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1844.NeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_non_barrel_roller_bearing(self) -> '_1845.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1845.NonBarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_roller_bearing(self) -> '_1846.RollerBearing':
        '''RollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1846.RollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_rolling_bearing(self) -> '_1849.RollingBearing':
        '''RollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1849.RollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_self_aligning_ball_bearing(self) -> '_1850.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.SelfAligningBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_spherical_roller_bearing(self) -> '_1852.SphericalRollerBearing':
        '''SphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1852.SphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_spherical_roller_thrust_bearing(self) -> '_1853.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1853.SphericalRollerThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_taper_roller_bearing(self) -> '_1854.TaperRollerBearing':
        '''TaperRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1854.TaperRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TaperRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_three_point_contact_ball_bearing(self) -> '_1855.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1855.ThreePointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_thrust_ball_bearing(self) -> '_1856.ThrustBallBearing':
        '''ThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1856.ThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_toroidal_roller_bearing(self) -> '_1857.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.ToroidalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_pad_fluid_film_bearing(self) -> '_1870.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1870.PadFluidFilmBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_grease_filled_journal_bearing(self) -> '_1872.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_journal_bearing(self) -> '_1874.PlainJournalBearing':
        '''PlainJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.PlainJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_oil_fed_journal_bearing(self) -> '_1876.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.PlainOilFedJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_tilting_pad_journal_bearing(self) -> '_1877.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.TiltingPadJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_tilting_pad_thrust_bearing(self) -> '_1878.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1878.TiltingPadThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_axial_clearance_bearing(self) -> '_1880.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.ConceptAxialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_clearance_bearing(self) -> '_1881.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1881.ConceptClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_radial_clearance_bearing(self) -> '_1882.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.ConceptRadialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Bearing.__class__)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def ring_results(self) -> 'List[_1762.RingForceAndDisplacement]':
        '''List[RingForceAndDisplacement]: 'RingResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingResults, constructor.new(_1762.RingForceAndDisplacement))
        return value

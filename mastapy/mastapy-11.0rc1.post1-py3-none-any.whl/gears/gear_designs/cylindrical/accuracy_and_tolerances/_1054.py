'''_1054.py

ISO1328AccuracyGrader
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1050
from mastapy._internal.python_net import python_net_import

_ISO1328_ACCURACY_GRADER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'ISO1328AccuracyGrader')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO1328AccuracyGrader',)


class ISO1328AccuracyGrader(_1050.CylindricalAccuracyGraderWithProfileFormAndSlope):
    '''ISO1328AccuracyGrader

    This is a mastapy class.
    '''

    TYPE = _ISO1328_ACCURACY_GRADER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO1328AccuracyGrader.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_helix_deviation(self) -> 'float':
        '''float: 'TotalHelixDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalHelixDeviation

    @property
    def total_profile_deviation(self) -> 'float':
        '''float: 'TotalProfileDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalProfileDeviation

    @property
    def single_pitch_deviation_iso(self) -> 'float':
        '''float: 'SinglePitchDeviationISO' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SinglePitchDeviationISO

    @property
    def cumulative_pitch_deviation(self) -> 'float':
        '''float: 'CumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CumulativePitchDeviation

    @property
    def total_cumulative_pitch_deviation(self) -> 'float':
        '''float: 'TotalCumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalCumulativePitchDeviation

    @property
    def total_radial_composite_deviation(self) -> 'float':
        '''float: 'TotalRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalRadialCompositeDeviation

    @property
    def toothto_tooth_radial_composite_deviation(self) -> 'float':
        '''float: 'ToothtoToothRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothtoToothRadialCompositeDeviation

    @property
    def runout(self) -> 'float':
        '''float: 'Runout' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Runout

    @property
    def helix_form_deviation(self) -> 'float':
        '''float: 'HelixFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixFormDeviation

    @property
    def helix_slope_deviation(self) -> 'float':
        '''float: 'HelixSlopeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixSlopeDeviation

    @property
    def profile_form_deviation(self) -> 'float':
        '''float: 'ProfileFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProfileFormDeviation

    @property
    def profile_slope_deviation(self) -> 'float':
        '''float: 'ProfileSlopeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProfileSlopeDeviation

    @property
    def base_pitch_deviation(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BasePitchDeviation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BasePitchDeviation) if self.wrapped.BasePitchDeviation else None

    @base_pitch_deviation.setter
    def base_pitch_deviation(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.BasePitchDeviation = value

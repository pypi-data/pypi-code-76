'''_1275.py

FourierSeries
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1278
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FOURIER_SERIES = python_net_import('SMT.MastaAPI.MathUtility', 'FourierSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('FourierSeries',)


class FourierSeries(_0.APIBase):
    '''FourierSeries

    This is a mastapy class.
    '''

    TYPE = _FOURIER_SERIES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FourierSeries.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit

    @property
    def peakto_peak(self) -> 'float':
        '''float: 'PeaktoPeak' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeaktoPeak

    @property
    def first_harmonic(self) -> '_1278.HarmonicValue':
        '''HarmonicValue: 'FirstHarmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1278.HarmonicValue)(self.wrapped.FirstHarmonic) if self.wrapped.FirstHarmonic else None

    @property
    def second_harmonic(self) -> '_1278.HarmonicValue':
        '''HarmonicValue: 'SecondHarmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1278.HarmonicValue)(self.wrapped.SecondHarmonic) if self.wrapped.SecondHarmonic else None

    @property
    def third_harmonic(self) -> '_1278.HarmonicValue':
        '''HarmonicValue: 'ThirdHarmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1278.HarmonicValue)(self.wrapped.ThirdHarmonic) if self.wrapped.ThirdHarmonic else None

    @property
    def fourth_harmonic(self) -> '_1278.HarmonicValue':
        '''HarmonicValue: 'FourthHarmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1278.HarmonicValue)(self.wrapped.FourthHarmonic) if self.wrapped.FourthHarmonic else None

    @property
    def fifth_harmonic(self) -> '_1278.HarmonicValue':
        '''HarmonicValue: 'FifthHarmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1278.HarmonicValue)(self.wrapped.FifthHarmonic) if self.wrapped.FifthHarmonic else None

    @property
    def harmonics(self) -> 'List[_1278.HarmonicValue]':
        '''List[HarmonicValue]: 'Harmonics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Harmonics, constructor.new(_1278.HarmonicValue))
        return value

    @property
    def harmonics_with_zeros_truncated(self) -> 'List[_1278.HarmonicValue]':
        '''List[HarmonicValue]: 'HarmonicsWithZerosTruncated' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HarmonicsWithZerosTruncated, constructor.new(_1278.HarmonicValue))
        return value

    @property
    def mean_value(self) -> 'float':
        '''float: 'MeanValue' is the original name of this property.'''

        return self.wrapped.MeanValue

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def values(self) -> 'List[float]':
        '''List[float]: 'Values' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Values, float)
        return value

    def set_amplitude(self, harmonic: 'int', amplitude: 'float'):
        ''' 'SetAmplitude' is the original name of this method.

        Args:
            harmonic (int)
            amplitude (float)
        '''

        harmonic = int(harmonic)
        amplitude = float(amplitude)
        self.wrapped.SetAmplitude(harmonic if harmonic else 0, amplitude if amplitude else 0.0)

    def set_phase(self, harmonic: 'int', phase: 'float'):
        ''' 'SetPhase' is the original name of this method.

        Args:
            harmonic (int)
            phase (float)
        '''

        harmonic = int(harmonic)
        phase = float(phase)
        self.wrapped.SetPhase(harmonic if harmonic else 0, phase if phase else 0.0)

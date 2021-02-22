'''_1723.py

LoadedRollerBearingResults
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1727
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLER_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedRollerBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollerBearingResults',)


class LoadedRollerBearingResults(_1727.LoadedRollingBearingResults):
    '''LoadedRollerBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_ROLLER_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedRollerBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hertzian_contact_width_inner(self) -> 'float':
        '''float: 'HertzianContactWidthInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthInner

    @property
    def hertzian_contact_width_outer(self) -> 'float':
        '''float: 'HertzianContactWidthOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthOuter

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        '''float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressOuter

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        '''float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressInner

'''_1746.py

Viscosities
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1740, _1742
from mastapy._internal.python_net import python_net_import

_VISCOSITIES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Viscosities')


__docformat__ = 'restructuredtext en'
__all__ = ('Viscosities',)


class Viscosities(_1742.SKFCalculationResult):
    '''Viscosities

    This is a mastapy class.
    '''

    TYPE = _VISCOSITIES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Viscosities.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def viscosity_ratio(self) -> 'float':
        '''float: 'ViscosityRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ViscosityRatio

    @property
    def operating_viscosity(self) -> '_1740.OperatingViscosity':
        '''OperatingViscosity: 'OperatingViscosity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1740.OperatingViscosity)(self.wrapped.OperatingViscosity) if self.wrapped.OperatingViscosity else None

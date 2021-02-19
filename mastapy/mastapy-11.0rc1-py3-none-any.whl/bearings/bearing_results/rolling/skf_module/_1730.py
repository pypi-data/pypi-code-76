'''_1730.py

Friction
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1731, _1732, _1741
from mastapy._internal.python_net import python_net_import

_FRICTION = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Friction')


__docformat__ = 'restructuredtext en'
__all__ = ('Friction',)


class Friction(_1741.SKFCalculationResult):
    '''Friction

    This is a mastapy class.
    '''

    TYPE = _FRICTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Friction.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power_loss(self) -> 'float':
        '''float: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerLoss

    @property
    def frictional_moment(self) -> '_1731.FrictionalMoment':
        '''FrictionalMoment: 'FrictionalMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1731.FrictionalMoment)(self.wrapped.FrictionalMoment) if self.wrapped.FrictionalMoment else None

    @property
    def friction_sources(self) -> '_1732.FrictionSources':
        '''FrictionSources: 'FrictionSources' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1732.FrictionSources)(self.wrapped.FrictionSources) if self.wrapped.FrictionSources else None

'''_1727.py

BearingRatingLife
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1737, _1741
from mastapy._internal.python_net import python_net_import

_BEARING_RATING_LIFE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'BearingRatingLife')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRatingLife',)


class BearingRatingLife(_1741.SKFCalculationResult):
    '''BearingRatingLife

    This is a mastapy class.
    '''

    TYPE = _BEARING_RATING_LIFE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingRatingLife.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def skf_life_modification_factor(self) -> 'float':
        '''float: 'SKFLifeModificationFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SKFLifeModificationFactor

    @property
    def contamination_factor(self) -> 'float':
        '''float: 'ContaminationFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContaminationFactor

    @property
    def life_model(self) -> '_1737.LifeModel':
        '''LifeModel: 'LifeModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1737.LifeModel)(self.wrapped.LifeModel) if self.wrapped.LifeModel else None

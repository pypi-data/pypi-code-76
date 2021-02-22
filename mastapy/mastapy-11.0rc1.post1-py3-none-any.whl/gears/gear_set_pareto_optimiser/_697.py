'''_697.py

ParetoFaceRatingOptimisationStrategyDatabase
'''


from mastapy.math_utility.optimisation import _1125
from mastapy._internal.python_net import python_net_import

_PARETO_FACE_RATING_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoFaceRatingOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoFaceRatingOptimisationStrategyDatabase',)


class ParetoFaceRatingOptimisationStrategyDatabase(_1125.ParetoOptimisationStrategyDatabase):
    '''ParetoFaceRatingOptimisationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _PARETO_FACE_RATING_OPTIMISATION_STRATEGY_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoFaceRatingOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

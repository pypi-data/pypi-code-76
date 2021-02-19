'''_1899.py

ConicalGearOptimisationStrategy
'''


from mastapy.system_model.optimization import _1908, _1900
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'ConicalGearOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearOptimisationStrategy',)


class ConicalGearOptimisationStrategy(_1908.OptimizationStrategy['_1900.ConicalGearOptimizationStep']):
    '''ConicalGearOptimisationStrategy

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_OPTIMISATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

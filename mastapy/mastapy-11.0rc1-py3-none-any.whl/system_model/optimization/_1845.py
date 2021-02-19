'''_1845.py

OptimizationStrategyDatabase
'''


from mastapy.utility.databases import _1348
from mastapy.system_model.optimization import _1837
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStrategyDatabase',)


class OptimizationStrategyDatabase(_1348.NamedDatabase['_1837.CylindricalGearOptimisationStrategy']):
    '''OptimizationStrategyDatabase

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_STRATEGY_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

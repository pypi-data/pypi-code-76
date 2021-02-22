'''_94.py

DynamicSolver
'''


from mastapy.nodal_analysis.system_solvers import _108
from mastapy._internal.python_net import python_net_import

_DYNAMIC_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'DynamicSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicSolver',)


class DynamicSolver(_108.StiffnessSolver):
    '''DynamicSolver

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_SOLVER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

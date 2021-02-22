'''_1408.py

BackwardEulerTransientSolver
'''


from mastapy.nodal_analysis.system_solvers import _1418
from mastapy._internal.python_net import python_net_import

_BACKWARD_EULER_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'BackwardEulerTransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('BackwardEulerTransientSolver',)


class BackwardEulerTransientSolver(_1418.SimpleVelocityBasedStepHalvingTransientSolver):
    '''BackwardEulerTransientSolver

    This is a mastapy class.
    '''

    TYPE = _BACKWARD_EULER_TRANSIENT_SOLVER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BackwardEulerTransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

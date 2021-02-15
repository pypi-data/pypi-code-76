import os
from pm4pycvxopt import util

from pm4pycvxopt.util.lp.versions import cvxopt_solver, cvxopt_solver_custom_align, cvxopt_solver_custom_align_ilp, cvxopt_solver_custom_align_arm

custom_solver = cvxopt_solver_custom_align
try:
    # for ARM-based Linux, we need to use a different call to GLPK
    if "arm" in str(os.uname()[-1]):
        custom_solver = cvxopt_solver
except:
    pass

from pm4py.util.lp import solver as solver

solver.CVXOPT = "cvxopt"
solver.CVXOPT_SOLVER_CUSTOM_ALIGN = "cvxopt_solver_custom_align"
solver.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP = "cvxopt_solver_custom_align_ilp"

solver.VERSIONS_APPLY[solver.CVXOPT] = cvxopt_solver.apply
solver.VERSIONS_GET_PRIM_OBJ[solver.CVXOPT] = cvxopt_solver.get_prim_obj_from_sol
solver.VERSIONS_GET_POINTS_FROM_SOL[solver.CVXOPT] = cvxopt_solver.get_points_from_sol

solver.VERSIONS_APPLY[solver.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.apply
solver.VERSIONS_GET_PRIM_OBJ[solver.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_prim_obj_from_sol
solver.VERSIONS_GET_POINTS_FROM_SOL[solver.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_points_from_sol

solver.VERSIONS_APPLY[solver.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.apply
solver.VERSIONS_GET_PRIM_OBJ[solver.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_prim_obj_from_sol
solver.VERSIONS_GET_POINTS_FROM_SOL[
    solver.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_points_from_sol
solver.DEFAULT_LP_SOLVER_VARIANT = solver.CVXOPT_SOLVER_CUSTOM_ALIGN


__version__ = '0.0.11'
__doc__ = "Process Mining for Python - CVXOpt Support"
__author__ = 'PADS'
__author_email__ = 'pm4py@pads.rwth-aachen.de'
__maintainer__ = 'PADS'
__maintainer_email__ = "pm4py@pads.rwth-aachen.de"

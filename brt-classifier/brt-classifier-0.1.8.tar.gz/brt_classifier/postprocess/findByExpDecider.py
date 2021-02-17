from rooted_tree_classifier import is_log_solvable, is_log_star_solvable
from ..complexity import complexities
from ..complexity import *

def findByExpDecider(problem, idx, data):
  constraints = set(problem["constraint"])
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if upperBound == UNKNOWN or lowerBound == UNKNOWN:
    decidedUpperBound = upperBound
    decidedLowerBound = lowerBound

    if is_log_star_solvable(constraints):
      decidedUpperBound = complexities[min(complexities.index(decidedUpperBound) if decidedUpperBound != UNKNOWN else 100, complexities.index(ITERATED_LOG))]
    else:
      decidedLowerBound = complexities[max(complexities.index(decidedLowerBound) if decidedLowerBound != UNKNOWN else -1, complexities.index(LOGLOG))]

    if is_log_solvable(constraints):
      decidedUpperBound = complexities[min(complexities.index(decidedUpperBound) if decidedUpperBound != UNKNOWN else 100, complexities.index(LOG))]
    else:
      decidedLowerBound = complexities[max(complexities.index(decidedLowerBound) if decidedLowerBound != UNKNOWN else -1, complexities.index(GLOBAL))]

    if (lowerBound != decidedLowerBound or upperBound != decidedUpperBound):
      data[idx]["lower-bound"] = decidedLowerBound
      data[idx]["upper-bound"] = decidedUpperBound
      print(constraints, lowerBound, upperBound, decidedLowerBound, decidedUpperBound)
      return 1

  return 0

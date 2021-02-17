from rooted_tree_classifier import is_log_solvable, is_log_star_solvable
from ..complexity import complexities
from ..complexity import *

def findContradictionsByDecider(problem, idx, data):
  constraints = set(problem["constraint"])
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if upperBound != UNSOLVABLE or lowerBound != UNSOLVABLE:

    if is_log_star_solvable(constraints) and lowerBound != UNKNOWN and complexities.index(lowerBound) > complexities.index(ITERATED_LOG):
      print(constraints, "lower-bound", lowerBound, "but log* solvable")
      return 1
    elif not is_log_star_solvable(constraints) and upperBound != UNKNOWN and complexities.index(upperBound) <= complexities.index(ITERATED_LOG):
      print(constraints, "upper-bound", upperBound, "but NOT log* solvable")
      return 1

    if is_log_solvable(constraints) and lowerBound != UNKNOWN and complexities.index(lowerBound) > complexities.index(LOG):
      print(constraints, "lower-bound", lowerBound, "but log solvable")
      return 1
    elif not is_log_solvable(constraints) and upperBound != UNKNOWN and complexities.index(upperBound) <= complexities.index(LOG):
      print(constraints, "upper-bound", upperBound, "but NOT log solvable")
      return 1

  return 0

from ..complexity import *

def findUpperBounds(problem, idx, data):
  constrs = set(problem["constraint"])
  upperBound = problem["upper-bound"]

  if upperBound == UNKNOWN:
    prevProblems = data[:idx]
    for prevProblem in prevProblems:
      prevConstrs = set(prevProblem["constraint"])
      prevUpperBound = prevProblem["upper-bound"]

      if (prevUpperBound != UNKNOWN and
         prevUpperBound != GLOBAL and
         prevUpperBound != GLOBAL and
         prevUpperBound != UNSOLVABLE and
         prevConstrs.issubset(constrs)):
        data[idx]["upper-bound"] = prevUpperBound
        print(constrs, prevUpperBound)
        return 1

  return 0

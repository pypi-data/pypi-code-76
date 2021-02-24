from ..complexity import *

def findLowerBounds(problem, idx, data):
  constrs = set(problem["constraint"])
  lowerBound = problem["lower-bound"]

  if lowerBound == UNKNOWN:
    prevProblems = data[idx+1:]
    for prevProblem in prevProblems:
      prevConstrs = set(prevProblem["constraint"])
      prevLowerBound = prevProblem["lower-bound"]

      if prevLowerBound != UNKNOWN and prevLowerBound != CONST and prevLowerBound != CONST and prevLowerBound != UNSOLVABLE and constrs.issubset(prevConstrs):
        data[idx]["lower-bound"] = prevLowerBound
        print(constrs, prevConstrs, prevLowerBound)
        return 1

  return 0

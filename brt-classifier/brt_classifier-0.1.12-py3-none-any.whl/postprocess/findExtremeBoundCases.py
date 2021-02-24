from ..complexity import *

def findExtremeBoundCases(problem, idx, data):
  constrs = problem["constraint"]
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if lowerBound == GLOBAL and upperBound == UNKNOWN:
    print(constrs, "Θ(n)")
    data[idx]["upper-bound"] = lowerBound
    return 1
  elif upperBound == CONST and lowerBound == UNKNOWN:
    print(constrs, "Θ(1)")
    data[idx]["lower-bound"] = upperBound
    return 1
  
  return 0

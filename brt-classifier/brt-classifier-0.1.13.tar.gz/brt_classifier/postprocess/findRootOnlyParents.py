from ..util import flatMap
from ..complexity import *

def findRootOnlyParents(problem, idx, data):
  constrs = problem["constraint"]
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if lowerBound == UNKNOWN or upperBound == UNKNOWN:
    parents = set([x[1] for x in constrs])
    children = set(flatMap(lambda x: [x[0], x[2]], constrs))
    if not parents.issubset(children):
      prunedConstrs = [x for x in constrs if x[1] != "3"]
      prevProblems = data[:idx]
      for prevProblem in prevProblems:
        prevConstrs = prevProblem["constraint"]
        if prevConstrs == prunedConstrs:
          print(constrs, prevProblem["lower-bound"], prevProblem["upper-bound"])
          data[idx]["lower-bound"] = prevProblem["lower-bound"]
          data[idx]["upper-bound"] = prevProblem["upper-bound"]
          break

      return 1

  return 0


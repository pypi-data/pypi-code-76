from ..complexity import *

def getMaximal(problem, idx, data):
  constrs = set(problem["constraint"])
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if lowerBound != UNKNOWN and upperBound != UNKNOWN:
    return 0

  prevProblems = data[idx+1:]
  for prevProblem in prevProblems:
    prevConstrs = set(prevProblem["constraint"])
    prevLowerBound = prevProblem["lower-bound"]
    prevUpperBound = prevProblem["upper-bound"]

    if prevLowerBound != UNKNOWN and prevUpperBound != UNKNOWN:
      for c in prevConstrs:
        prevConstrs.remove(c)
        if constrs == prevConstrs and c != c[0] * len(c):
          prevConstrs.add(c)
          print(constrs, prevConstrs, c, prevProblem["lower-bound"], prevProblem["upper-bound"])
          break

        prevConstrs.add(c)

  return 0

if __name__ == "__main__":
  postprocess(getMaximal)

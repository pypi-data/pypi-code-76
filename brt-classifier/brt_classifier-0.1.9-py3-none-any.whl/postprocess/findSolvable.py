from ..util import getCanonical, flatMap
from ..complexity import *

def findSolvableByCyclePathClassifier(problem, idx, data):
  problemId = problem["id"]
  constrs = problem["constraint"]
  lowerBound = problem["lower-bound"]
  upperBound = problem["upper-bound"]

  if lowerBound != UNKNOWN and upperBound != UNKNOWN:
    return 0

  # TODO: refactor the mess below
  parentChildPairs = sorted(list(set(flatMap(lambda x: [x[0:2][::-1], x[1:]], constrs))))
  lastParent = ""
  childrenOfTheSameParent = []
  canUse = True
  ctr = 0
  
  for pair in parentChildPairs:
    p = pair[0]
    c = pair[1]
    if (c + p + c) in constrs:
      if lastParent == p:
        if len([x for x in childrenOfTheSameParent if not (getCanonical(x + p + c) in constrs)]) == 0:
          ctr += 1
          ctr += len(childrenOfTheSameParent)
          childrenOfTheSameParent.append(c)
        else:
          canUse = False
          break
      else:
        lastParent = p
        childrenOfTheSameParent = [c]
        ctr += 1
    else:
      canUse = False
      break
    
  if canUse and ctr == len(constrs):
    print(constrs, problemId)
    return 1

  return 0

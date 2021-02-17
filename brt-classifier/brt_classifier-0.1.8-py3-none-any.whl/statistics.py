import json
from .complexity import *

def printStatistics(filePath):
  with open(filePath) as json_file:
    data = json.load(json_file)

    lowerBoundConstant = 0
    upperBoundConstant = 0
    constSolvable = 0

    lowerBoundLogStar = 0
    upperBoundLogStar = 0
    logStarSolvable = 0

    lowerBoundLoglog = 0
    upperBoundLoglog = 0
    loglogSolvable = 0

    lowerBoundLog = 0
    upperBoundLog = 0
    logSolvable = 0

    lowerBoundLinear = 0
    upperBoundLinear = 0
    linearSolvable = 0

    unsolvable = 0

    for p in data:
      lowerBound = p["lower-bound"]
      upperBound = p["upper-bound"]

      if lowerBound == CONST:
        lowerBoundConstant += 1
      if upperBound == CONST:
        upperBoundConstant += 1
      if lowerBound == CONST and upperBound == CONST:
        constSolvable += 1

      if lowerBound == ITERATED_LOG:
        lowerBoundLogStar += 1
      if upperBound == ITERATED_LOG:
        upperBoundLogStar += 1
      if lowerBound == ITERATED_LOG and upperBound == ITERATED_LOG:
        logStarSolvable += 1

      if lowerBound == LOGLOG:
        lowerBoundLoglog += 1
      if upperBound == LOGLOG:
        upperBoundLoglog += 1
      if lowerBound == LOGLOG and upperBound == LOGLOG:
        loglogSolvable += 1

      if lowerBound == LOG:
        lowerBoundLog += 1
      if upperBound == LOG:
        upperBoundLog += 1
      if lowerBound == LOG and upperBound == LOG:
        logSolvable += 1

      if lowerBound == GLOBAL:
        lowerBoundLinear += 1
      if upperBound == GLOBAL:
        upperBoundLinear += 1
      if lowerBound == GLOBAL and upperBound == GLOBAL:
        linearSolvable += 1

      if lowerBound == UNSOLVABLE:
        unsolvable += 1

    totalSize = len(data)

    print("In total: %s problems" % totalSize)
    print("Solvable in constant time: %s " % constSolvable)
    print("Solvable in log* time: %s " % logStarSolvable)
    print("Solvable in loglog time: %s " % loglogSolvable)
    print("Solvable in log time: %s " % logSolvable)
    print("Solvable in linear time: %s " % linearSolvable)
    print("Unsolvable: %s" % unsolvable)
    print("TBD: %s" % (totalSize - unsolvable - constSolvable - logStarSolvable - loglogSolvable - logSolvable - linearSolvable))
    print()

    print("Lower bounds")
    print("Constant time: %s " % lowerBoundConstant)
    print("Log* time: %s " % lowerBoundLogStar)
    print("Loglog time: %s " % lowerBoundLoglog)
    print("Log time: %s " % lowerBoundLog)
    print("Linear time: %s " % lowerBoundLinear)
    print("TBD: %s" % (totalSize - unsolvable - lowerBoundConstant - lowerBoundLogStar - lowerBoundLoglog - lowerBoundLog - lowerBoundLinear))
    print()

    print("Upper bounds")
    print("Constant time: %s " % upperBoundConstant)
    print("Log* time: %s " % upperBoundLogStar)
    print("Loglog time: %s " % upperBoundLoglog)
    print("Log time: %s " % upperBoundLog)
    print("Linear time: %s " % upperBoundLinear)
    print("TBD: %s" % (totalSize - unsolvable - upperBoundConstant - upperBoundLogStar - upperBoundLoglog - upperBoundLog - upperBoundLinear))

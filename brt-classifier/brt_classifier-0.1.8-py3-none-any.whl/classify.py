from .postprocess.postprocess import postprocess as doPostprocess
from .postprocess.findExtremeBoundCases import findExtremeBoundCases
from .postprocess.findLogLowerBounds import findLogLowerBounds
from .postprocess.findLowerBounds import findLowerBounds
from .postprocess.findLowerBoundsByReplacement import findLowerBoundsByReplacement
from .postprocess.findSolvable import findSolvableByCyclePathClassifier
from .postprocess.findUpperBounds import findUpperBounds
from .postprocess.findRootOnlyParents import findRootOnlyParents
from .postprocess.findByExpDecider import findByExpDecider
from .postprocess.findContradictionsByDecider import findContradictionsByDecider

def classify(filePath, persist):
  updateCtr = 1
  while updateCtr != 0:
    updateCtr = 0

    print("Problems that contradict Jan's exponential algorithm")
    updateCtr += doPostprocess(findContradictionsByDecider, filePath, persist)
    print()

    print("Problems decidable by Jan's exponential algorithm")
    updateCtr += doPostprocess(findByExpDecider, filePath, persist)
    print()

    print("Problems where 3 can only be at the root")
    updateCtr += doPostprocess(findRootOnlyParents, filePath, persist)
    print()

    print("Upper bounds using relaxations of known problems")
    updateCtr += doPostprocess(findUpperBounds, filePath, persist)
    print()

    print("Problems solvable by cyclepath classifier")
    updateCtr += doPostprocess(findSolvableByCyclePathClassifier, filePath, persist)
    print()

    print("Lower bounds using restrictions of known problems")
    updateCtr += doPostprocess(findLowerBounds, filePath, persist)
    print()

    print("Lower bounds by \"if I replace x wtih y, we get known problem => at least as hard\"")
    updateCtr += doPostprocess(findLowerBoundsByReplacement, filePath, persist)
    print()

    print("Log lower bounds if children uniquely determine their parents")
    updateCtr += doPostprocess(findLogLowerBounds, filePath, persist)
    print()

    print("If lower-bound is linear, upper is linear. If upper is constant, lower is constant")
    updateCtr += doPostprocess(findExtremeBoundCases, filePath, persist)
    print()

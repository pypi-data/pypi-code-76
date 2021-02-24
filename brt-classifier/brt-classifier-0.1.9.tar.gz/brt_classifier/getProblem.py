import os, json
from tqdm import tqdm
from .util import flatMap, getCanonical
from .generateProblems import getIsomorphism, pruneSet
from .complexity import UNSOLVABLE

def loadAndScanProblems(json_file, constraints, colorCount):
  data = json.load(json_file)
  canonicalConstrSet = {getCanonical(x) for x in constraints}
  for _ in range(colorCount-1):
    canonicalConstrSet = pruneSet(canonicalConstrSet)
  ismrs = getIsomorphism(set(canonicalConstrSet), colorCount)
  for problem in data:
    if set(problem['constraint']) in ismrs:
      return problem

  return {
    "constraint": sorted(list(canonicalConstrSet)),
    "upper-bound": UNSOLVABLE,
    "lower-bound": UNSOLVABLE,
    "unsolvable-count": "",
    "solvable-count": "",
    "id": -1
  }

def findProblem(data, constraints, colorCount):
  canonicalConstrSet = {getCanonical(x) for x in constraints}
  for _ in range(colorCount-1):
    canonicalConstrSet = pruneSet(canonicalConstrSet)
  ismrs = getIsomorphism(set(canonicalConstrSet), colorCount)

  for ismr in ismrs:
    key = tuple(sorted(list(ismr)))
    if key in data:
      return data[key]

  return {
    "constraint": sorted(list(canonicalConstrSet)),
    "upper-bound": UNSOLVABLE,
    "lower-bound": UNSOLVABLE,
    "unsolvable-count": "",
    "solvable-count": "",
    "id": -1
  }

def loadAndBatchScan(json_file, constraintsList, colorCount):
  data = json.load(json_file)
  data = {tuple(d['constraint']): d for d in data}
  return [findProblem(data, c, colorCount) for c in tqdm(constraintsList)]

def getProblems(constraintsList):
  representativeC = constraintsList[0]
  alphabet = set(flatMap(lambda x: x, list(representativeC)))
  labelCount = len(alphabet)
  if labelCount == 2:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/2labels.json') as json_file:
      return loadAndBatchScan(json_file, constraintsList, labelCount)
  elif labelCount == 3:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/3labels.json') as json_file:
      return loadAndBatchScan(json_file, constraintsList, labelCount)
  else:
    raise Exception('Only problems with 2 or 3 labels are supported')
  
  canonicalConstrSet = pruneSet({getCanonical(x) for x in constraints})
  ismrs = getIsomorphism(set(canonicalConstrSet), colorCount)
  for problem in data:
    if set(problem['constraint']) in ismrs:
      return problem

def getProblem(constraints):
  alphabet = set(flatMap(lambda x: x, list(constraints)))
  labelCount = len(alphabet)

  if labelCount == 2:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/2labels.json') as json_file:
      return loadAndScanProblems(json_file, constraints, labelCount)
  elif labelCount == 3:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/problems/3labels.json') as json_file:
      return loadAndScanProblems(json_file, constraints, labelCount)
  else:
    raise Exception('Only problems with 2 or 3 labels are supported')

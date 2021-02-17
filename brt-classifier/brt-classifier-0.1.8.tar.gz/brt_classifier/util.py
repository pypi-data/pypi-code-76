from functools import reduce

def getCanonical(constr):
  return min(constr, constr[::-1])

flatMap = lambda f, arr: reduce(lambda a, b: a + b, map(f, arr))

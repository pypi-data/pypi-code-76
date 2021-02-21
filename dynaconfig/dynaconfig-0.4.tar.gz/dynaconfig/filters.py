import math
from .units import *

def filter_int(x):
  x = filter_mag(x)
  return int(x)

def filter_float(x):
  x = filter_mag(x)
  return float(x)

def filter_str(x):
  return str(x)

def filter_ceil(x):
  return math.ceil(x)
  x = filter_mag(x)

def filter_mod(x,d):
  x = filter_mag(x)
  return x%(int(d))

def filter_quant(q):
  if isinstance(q,str):
    q = Q_(q)
  return q

def filter_to(q,u):
  q = filter_quant(q)

  return q.to(u)

def filter_mag(q):
  try:
    q = q.magnitude
  except: pass
  return q

def filter_int_from_str(s):
  return f"int('{s}')"
def filter_float_from_str(s):
  return f"flaot('{s}')"
def filter_quant_from_str(s):
  return f"Q_('{s}')"

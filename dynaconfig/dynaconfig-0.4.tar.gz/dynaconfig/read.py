from .render import render_tree, CircularDependency
from .file_parsers import *

import re


funcRegex = re.compile(r'^\s*([^\s\(]+)\(([^\)]*)\)\s*')

def include_func(fn, context):
  with open(fn) as f:
    text = f.read()
  return context['parser'](text)

def DataTable_func(fn, context):
  return DataTable(fn)
  
funcs = { 'include' : include_func
        , 'DataTable' : DataTable_func }

def get_func_and_args(v):
  if not isinstance(v,str):
    return None,None

  m = funcRegex.match(v)
  if m is None:
    return None,None
    
  f = m.groups()[0].strip(''' \t\n'"''')
  a = m.groups()[1].split(',')
  for i in range(len(a)):
    a[i] = eval(a[i].strip())

  return f,a


def readConfig( text = None, parser = yaml.safe_load
                           , render = True
                           , ignore_unparsed_expressions = False
                           , return_fspathtree = False
                           , filters = {}
                           , filename = None
                           , debug = False):
  '''
  Read string (or file) containing configuration data into a data tree.

  :param text: String containing configuration file text
  
  :param parser: A callable that can parse the configuration text into a configuration tree. For example,
  ``parser=yaml.safe_load`` or ``parser=json.loads``.

  :param render: Attempt to render the configuration tree.

  :param filename: Configuration filename. If given, ``text`` parameter is ignored.

  '''
  # if a filename is given, read it into the text string
  if filename:
    with open(filename) as f:
      text = f.read()

  # read the data from the string into a tree
  data = fspathtree(parser(text))

  # if render is set, we want to render the data tree
  if render:
    data = render_tree( data, strict=not ignore_unparsed_expressions, filters=filters )

  if return_fspathtree:
    return data

  return data.tree

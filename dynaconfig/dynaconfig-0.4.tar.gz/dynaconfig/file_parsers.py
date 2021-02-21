from .utils import *

'''
Some extra file parsing classes to handle simple config file formats like ini and key=val.
'''

import re
import io
import configparser
from fspathtree import fspathtree

import yaml
import json

class ini:
  @staticmethod
  def load( text ):
    parser = configparser.ConfigParser()
    f = io.StringIO(text)
    parser.read_file( f )
    f.close()

    data = dict()
    for sec in parser.sections():
      data[sec] = dict()
      for opt in parser.options(sec):
        data[sec][opt] = parser.get( sec, opt )

      
    return data


  @staticmethod
  def dump( data ):
    print("ini dump not implemented yet")

class keyval:
  '''A simple key=val style parser.'''

  @staticmethod
  def load( text ):
    data = dict()
    for line in text.split('\n'):
      line = line.strip()
      if len(line) < 1 or line[0] == '#':
        continue

      tokens = line.split('=')
      if len(tokens) < 2:
        raise RuntimeError("Syntax Error: key (%s) found with no value. Expect 'key=val' format" % tokens[0])

      key = tokens[0]
      val = '='.join( tokens[1:] )
      val = val.split('#')[0] # throw away comments

      key = key.strip()
      val = val.strip()

      fspathtree.setitem(data,key,val)

    return data

  @staticmethod
  def dump( data ):
    tree = fspathtree(data)
    text = ""
    for p in tree.get_all_leaf_node_paths():
      text += str(p.relative_to('/'))
      text += " = "
      text += str( tree[p] )
      text += "\n"

    return text

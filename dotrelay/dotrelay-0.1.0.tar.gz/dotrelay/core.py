import logging
log = logging.getLogger("📡dotrelay")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

import os
import sys

MAX_DEPTH = 10

# use context manager
class Relay():
  def __init__(self, path, max_depth=MAX_DEPTH):
    self.path = os.path.abspath(path)
    self.max_depth = max_depth
    self.mod_path = None
  
  def __enter__(self):
    curr_path = self.path
    for depth in range(0, self.max_depth):
      relay_file_path = os.path.join(curr_path, '.relay')
      if depth > 0 and os.path.exists(relay_file_path):
        log.debug(f'depth of {depth} reached - .relay file found in {self.mod_path} - adding to module import path...')
        self.mod_path = curr_path
        sys.path.append(self.mod_path)
        break
      else:
        log.debug(f'depth of {depth} reached - .relay file not found in {curr_path} - checking parent path...')
        curr_path = os.path.dirname(curr_path) # go up to parent path

    if not self.mod_path:    
      log.warn(f'max depth of {depth} reached - .relay file not found in any ancestor paths - no changes were made to module import path.')

  def __exit__(self, type, value, traceback):
    if self.mod_path:
      log.debug(f'finished relaying {self.mod_path} to {self.path} - removing from module import path...')
      sys.path.remove(self.mod_path)
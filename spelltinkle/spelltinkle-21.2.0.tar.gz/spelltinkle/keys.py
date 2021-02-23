from typing import Dict

keynames = {
    '^a': 'home',
    '^l': 'home',
    '^c': 'copy',
    '^d': 'delete',
    '^e': 'end',
    '^f': 'search_forward',
    '^g': 'code_analysis',
    '^h': 'help',
    '^i': 'tab',
    '^k': 'delete_to_end_of_line',
    '^n': 'down1',
    '^o': 'open',
    '^p': 'paste',
    '^q': 'quit',
    '^r': 'search_backward',
    '^s': 'write',
    '^t': 'swap',
    '^u': 'undo',
    '^v': 'view_files',
    '^w': 'mark_word',
    '^x': 'command',
    '^z': 'stop',
    '^ ': 'normalize_space'}

doubles: Dict[str, Dict[str, str]] = {
    '^b': {'^d': 'rectangle_delete',
           '^p': 'rectangle_insert',
           '<': 'dedent',
           '>': 'indent'},
    '^y': {'^b': 'go_to_bookmark',
           '^B': 'create_bookmark',
           '^f': 'format',
           '^g': 'jedi',  # goto def
           'i': 'isort',
           '^o': 'open_file_under_cursor',
           '^s': 'spell_check',
           '^y': 'complete',  # old complete
           '^u': 'usages',
           '^d': 'diff',
           '^m': 'macro',
           '^r': 'resolve_conflict',
           's': 'write_as',
           'S': 'write_force',
           'Q': 'quit_force',
           '+': 'upper',
           '-': 'lower',
           '8': 'yapf'}}

again = {'delete_to_end_of_line'}

repeat = {'home', 'end'}

typos = {'imoprt': 'import'}

aliases = {'np': 'import numpy as np',
           'plt': 'import matplotlib.pyplot as plt',
           'path': 'from pathlib import Path',
           'dd': 'from collections import defaultdict',
           'main': "if __name__ == '__main__':",
           'init': 'def __init__(self):',
           'hint': 'from typing import List'}

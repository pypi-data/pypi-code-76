# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyomino']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover==0.4.3', 'numpy>=1.20,<2.0', 'pretty-poly==0.2.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctests',
                     'test = run_tests:run_tests']}

setup_kwargs = {
    'name': 'polyomino',
    'version': '0.5.0a0',
    'description': 'Solve polyomino tiling problems.',
    'long_description': "# POLYOMINO - a Python package for polyomino tiling problems\n[![PyPI version](https://badge.fury.io/py/polyomino.svg)](https://badge.fury.io/py/polyomino)\n![Deploy wheels to pypi](https://github.com/jwg4/polyomino/workflows/Deploy%20wheels%20to%20pypi/badge.svg)\n![Run Python tests](https://github.com/jwg4/polyomino/workflows/Run%20Python%20tests/badge.svg)\n\n\nThis is a package for manipulating polyominos and in particular, solving tiling problems. It uses the 'exact-cover' python package as the main engine for solving cover problems.\n\nTo solve a tiling problem, you need to create a 'board', the set of squares to be covered, and a 'tileset', the collection of polyominos which can be used. There are examples of the syntax to do this in examples/fluid.md The example file examples/gardner.md uses the package to solve a number of problems from the chapter on polyominos from Martin Gardner's book 'Mathematical Puzzles and Diversions'.\n\nNote that each tile can play one of several roles in a tiling problem. It could be a tile which can only appear once, as in problems like covering a chessboard with one copy of each pentomino and a square tetromino. It could be a tile which can be used an arbitrary number of times. Problems like this are often simply to cover a shape completely with copies of a single polyomino. Finally, it could be used either once or not at all. When constructing a tileset, it is possible to include tiles in any of these three classes.\n\n## Design\nBoth polyominos and boards are represented internally as lists of integer tuples (x, y). There are constants defined for all polyominos up to pentominos in polyomino.constant\n\nThe search algorithm used for searching for tilings is 'Algorithm X', also known as 'Dancing Links' from the famous paper by Knuth (https://arxiv.org/abs/cs/0011047). The paper suggests polyomino tilings and related problems as examples of exact cover problems which can be solved by the algorithm. There are more details about how the algorithm works on the homepage of the exact-cover package, https://github.com/jwg4/exact-cover\n\nIn reducing a tiling problem to an exact cover problem, each square of the shape to be covered becomes a column of the problem. Each placement of a particular tile in a particular place is a row. A row has 1s in columns corresponding to all the squares which are covered by that shape in that location.\nThere can be additional columns which correspond to the use of a piece, if that piece can only be used once. Problems where each piece can be used an arbitrary number of times, do not have such columns.\n\nIn the case where all tiles must be used exactly once, we have as many columns as the number of squares to be covered plus the number of tiles to be used. As Knuth points out, when the algorithm looks for a column which can be covered in one way, this means it is finding either a square which needs a particular piece to cover it, or for a piece which can only be fitted on the board in one way. Both deductive strategies should be used to narrow down efficiently.\n\nA heuristic for searches involving a limited number of monominos (single squares) can be configured. In the future we hope to implement further search heuristic options, as well as alternative algorithms for special cases like domino tiling.\n",
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

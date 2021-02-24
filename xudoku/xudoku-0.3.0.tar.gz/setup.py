# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xudoku']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'xudoku',
    'version': '0.3.0',
    'description': "Solve sudoku using an 'exact cover' algorithm.",
    'long_description': "# xudoku - Solve sudoku using an 'exact cover' algorithm\n\nThis is the sudoku code from @moygit's project 'exact_cover_np'.\n\nThe package is maintained by me, @jwg4.\n\nI separated the code for the 'exact cover' algorithm (now available at https://github.com/jwg4/exact_cover) from the sudoku code and created this package.\n\n",
    'author': 'Moy Easwaran',
    'author_email': None,
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/jwg4/xudoku',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

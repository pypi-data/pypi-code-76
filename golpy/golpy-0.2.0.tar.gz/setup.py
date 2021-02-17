# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golpy']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0', 'numpy>=1.20.1,<2.0.0']

entry_points = \
{'console_scripts': ['life = golpy.__init__:main']}

setup_kwargs = {
    'name': 'golpy',
    'version': '0.2.0',
    'description': "Efficient Conway's Game of Life using NumPy",
    'long_description': "# GoLPy\n[![GitHub\nlicense](https://img.shields.io/github/license/Zeta611/golpy?style=flat-square)](https://github.com/Zeta611/golpy/blob/master/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/golpy?style=flat-square)](https://pypi.org/project/golpy/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n\nGoLPy is an efficient Conway's Game of Life implemented in Python using NumPy.\n\n## Example Output\nThe following GIF can be generated using the command:\n```sh\nlife --demo glidergun --out glider_gun.gif --ppc 10 --pos TL -W60 -H40\n```\n\n![The Gosper Glider Gun](glider_gun.gif)\n\n## Usage\n```\nusage: life [-h] (-i GRID_INPUT | -d DEMO) [-o FILE | --debug-print]\n            [-W WIDTH] [-H HEIGHT] [-M MAX_GEN] [--ppc PIXELS] [-P POSITION]\n            [-p]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i GRID_INPUT, --in GRID_INPUT\n                        Parse the initial grid from <GRID_INPUT>\n  -d DEMO, --demo DEMO  Try one of the provided demos: one of 'glidergun' and\n                        'glidergen'\n  -o FILE, --out FILE   Place the output into <FILE>\n  --debug-print         Print the generated frames directly to the terminal,\n                        instead of saving them\n\n  -W WIDTH, --width WIDTH\n                        Width of the grid\n  -H HEIGHT, --height HEIGHT\n                        Height of the grid\n\n  -M MAX_GEN, --max-gen MAX_GEN\n                        Number of generations to simulate\n  --ppc PIXELS          Set the width and the height of each cell to <PIXELS>\n  -P POSITION, --pos POSITION\n                        One of 'C', 'T', 'B', 'L', 'R', 'TL', 'TR', 'BL', and\n                        'BR'\n\n  -p, --profile         Measure the performance\n```\n\n## Input Format\n```\n........................O\n......................O.O\n............OO......OO............OO\n...........O...O....OO............OO\nOO........O.....O...OO\nOO........O...O.OO....O.O\n..........O.....O.......O\n...........O...O\n............OO\n```\n\nUse `.` for a dead cell, `O` (`chr(79)`) for a live cell.\n\n## License\n[MIT](LICENSE)\n",
    'author': 'Jay Lee',
    'author_email': 'jaeho.lee@snu.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zeta611/py-game-of-life',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

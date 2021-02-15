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
    'version': '0.1.1',
    'description': "Efficient Conway's Game of Life using NumPy",
    'long_description': "# GoLPy\nGoLPy is an efficient Conway's Game of Life implemented in Python using NumPy.\n\n## Example Output\nThe following GIF can be generated using the command:\n```sh\nlife --demo glidergun --out glider_gun.gif --ppc 10 --pos TL -W60 -H40\n```\n\n![The Gosper Glider Gun](glider_gun.gif)\n\n## Usage\n```\nusage: life [-h] (-i IN | -d DEMO) [-o OUT | --debug-print] [-W WIDTH] [-H HEIGHT] [-M MAX_GEN] [--ppc PPC] [-P POS] [-p]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i IN, --in IN\n  -d DEMO, --demo DEMO\n  -o OUT, --out OUT\n  --debug-print\n\n  -W WIDTH, --width WIDTH\n  -H HEIGHT, --height HEIGHT\n\n  -M MAX_GEN, --max-gen MAX_GEN\n  --ppc PPC\n  -P POS, --pos POS\n\n  -p, --profile\n```\n\n## Input Format\n```\n........................O\n......................O.O\n............OO......OO............OO\n...........O...O....OO............OO\nOO........O.....O...OO\nOO........O...O.OO....O.O\n..........O.....O.......O\n...........O...O\n............OO\n```\n\nUse `.` for a dead cell, `O` (`chr(79)`) for a live cell.\n\n## License\n[MIT](LICENSE)\n",
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concentration']

package_data = \
{'': ['*']}

install_requires = \
['hug>=2.6.1,<3.0.0']

entry_points = \
{'console_scripts': ['concentration = concentration.run:__hug__.cli']}

setup_kwargs = {
    'name': 'concentration',
    'version': '1.1.4',
    'description': "Get work done when you need to, goof off when you don't.",
    'long_description': "Concentration\n============================\n[![PyPI version](https://badge.fury.io/py/concentration.svg)](http://badge.fury.io/py/concentration)\n[![Test Status](https://github.com/timothycrosley/concentration/workflows/Test/badge.svg?branch=develop)](https://github.com/timothycrosley/concentration/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/timothycrosley/concentration/workflows/Lint/badge.svg?branch=develop)](https://github.com/timothycrosley/concentration/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/timothycrosley/concentration/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/concentration)\n[![Join the chat at https://gitter.im/timothycrosley/concentration](https://badges.gitter.im/timothycrosley/concentration.svg)](https://gitter.im/timothycrosley/concentration?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/concentration/)\n[![Downloads](https://pepy.tech/badge/concentration)](https://pepy.tech/project/concentration)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/concentration/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/concentration/)\n\nStay focused on work when you want, and goof off when you don't. Concentration is a simple\nPython 3 console utility to block distracting sites when you need to focus, while allowing you to easily\ntake timed breaks. Concentration uses the /etc/hosts file as the mechanism to\nblock sites, and works on Linux, Macintosh, and Windows.\n\n![Concentration Example](https://raw.github.com/timothycrosley/concentration/develop/example.gif)\n\n\nInstalling Concentration\n============================\n\n    pip3 install concentration\n\n    # Or if pip is already set to use Python 3\n    pip install concentration\n\n\nUsing Concentration\n============================\n\nTo keep focused (blocking distracting sites):\n\n    sudo concentration improve\n\nTo take a small 5 minute timed break:\n\n    sudo concentration break\n\nTo take a long 60 minute timed break:\n\n    sudo concentration break -m 60\n\nYou can cancel breaks with `Ctrl-C`.\n\nTo disable blocking until you explicitly enable it again:\n\n    sudo concentration lose\n\n\nConfiguring Concentration\n============================\n\nYou can add more files to the blocked list by putting them in the following files (new line delimited):\n- ~/.concentration.distractors\n- /etc/concentration.distractors\n\n\nYou can make sure sites are visible even if concentration is enabled by putting them in the following files (new line delimited):\n- ~/.concentration.safe\n- /etc/concentration.safe\n\n--------------------------------------------\n\nThanks and I hope you find concentration useful in your effort to get more done!\n\n~Timothy Crosley\n",
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

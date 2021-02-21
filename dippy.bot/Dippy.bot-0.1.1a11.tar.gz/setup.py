# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dippy', 'dippy.extensions', 'dippy.labels']

package_data = \
{'': ['*']}

install_requires = \
['bevy>=0.4.5,<0.5.0', 'discord.py>=1.6.0,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'dippy.bot',
    'version': '0.1.1a11',
    'description': 'A Discord bot framework built to simplify the complicated parts of bot development.',
    'long_description': 'A Discord bot framework built to simplify the complicated parts of bot development.\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/Dippy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

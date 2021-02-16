# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fiji_arnheim', 'fiji_arnheim.macros', 'fiji_arnheim.registries']

package_data = \
{'': ['*']}

install_requires = \
['bergen>=0.3.31,<0.4.0', 'grunnlag>=0.2.9,<0.3.0', 'pyimagej>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['fiji-arnheim = fiji_arnheim.run:main']}

setup_kwargs = {
    'name': 'fiji-arnheim',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

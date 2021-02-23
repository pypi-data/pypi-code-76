# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cocoro']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'fire>=0.4.0,<0.5.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['cocoro = cocoro:main']}

setup_kwargs = {
    'name': 'cocoro',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'rcmdnk',
    'author_email': 'rcmdnk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

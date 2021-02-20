# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['avault']

package_data = \
{'': ['*']}

install_requires = \
['ansible>=2.5,<3.0',
 'cryptography>=3.4.6,<4.0.0',
 'jinja2>=2.11.3,<3.0.0',
 'pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['avault = avault.avault:main']}

setup_kwargs = {
    'name': 'avault',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Shoma FUKUDA',
    'author_email': 'fkshom+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fkshom',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

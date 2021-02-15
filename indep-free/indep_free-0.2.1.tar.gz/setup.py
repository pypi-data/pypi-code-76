# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indep_free']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['indep_free = indep_free.cli:main']}

setup_kwargs = {
    'name': 'indep-free',
    'version': '0.2.1',
    'description': 'Send newspaper "El Independiente" to mail. While we can download the newspaper and sed via email.',
    'long_description': None,
    'author': 'Emmanuel Arias',
    'author_email': 'eamanu@yaerobi.com',
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

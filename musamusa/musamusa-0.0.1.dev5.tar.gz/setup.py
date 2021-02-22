# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.11.1,<10.0.0']

setup_kwargs = {
    'name': 'musamusa',
    'version': '0.0.1.dev5',
    'description': 'Tool to display annotated texts.',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

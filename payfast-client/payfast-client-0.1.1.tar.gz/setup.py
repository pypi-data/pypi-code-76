# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['payfast_client']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2021.1,<2022.0', 'requests-futures>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'payfast-client',
    'version': '0.1.1',
    'description': 'Python client for interacting with the Payfast API',
    'long_description': '# payfast-python-client\n\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0a0a2acf5df045ceb533c8ee953d23a2)](https://app.codacy.com/gh/fergusdixon/payfast-python-client?utm_source=github.com&utm_medium=referral&utm_content=fergusdixon/payfast-python-client&utm_campaign=Badge_Grade)\n\nPython Client for the Payfast API\n',
    'author': 'Fergus Strangways-Dixon',
    'author_email': 'fergusdixon101@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fergusdixon/payfast-python-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

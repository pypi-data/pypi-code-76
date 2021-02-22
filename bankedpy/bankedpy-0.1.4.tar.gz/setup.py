# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bankedpy', 'bankedpy.payment_session']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=1.1.2,<2.0.0',
 'iso4217>=1.6.20180829,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'bankedpy',
    'version': '0.1.4',
    'description': 'A python client for consuming Banked API',
    'long_description': '# BankedPy (In development)\n\nA python client for consuming Banked API using `pydantic` and `requests`',
    'author': 'Aryan Curiel',
    'author_email': 'aryan.curiel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acuriel/bankedpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

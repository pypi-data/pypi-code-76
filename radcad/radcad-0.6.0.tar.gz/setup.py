# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radcad',
 'radcad.backends',
 'radcad.compat.cadCAD',
 'radcad.compat.cadCAD.configuration',
 'radcad.compat.cadCAD.configuration.utils',
 'radcad.compat.cadCAD.engine',
 'radcad.extensions.backends']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0', 'pathos>=0.2.7,<0.3.0']

extras_require = \
{'compat': ['cadCAD>=0.4.23,<0.5.0'],
 'extension-backend-ray': ['ray>=1.1.0,<2.0.0', 'boto3>=1.16.43,<2.0.0']}

setup_kwargs = {
    'name': 'radcad',
    'version': '0.6.0',
    'description': 'A cadCAD implementation, for dynamical systems modelling & simulation',
    'long_description': None,
    'author': 'Benjamin Scholtz',
    'author_email': 'ben@bitsofether.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<=3.9',
}


setup(**setup_kwargs)

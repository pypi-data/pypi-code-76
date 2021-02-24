# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nomnomdata', 'nomnomdata.auth']

package_data = \
{'': ['*']}

install_requires = \
['dunamai>=1.1.0,<2.0.0',
 'nomnomdata-cli>=0.1.0,<0.2.0',
 'pycognito>=0.1.2,<0.2.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'nomnomdata.cli_plugins': ['login = nomnomdata.auth.cli:login']}

setup_kwargs = {
    'name': 'nomnomdata-auth',
    'version': '2.3.4.post3.dev0',
    'description': 'Handle authorization to Nom Nom Data services',
    'long_description': '# nomnomdata-auth\n\nTiny library that contains KeyAuth, a requests library authorizer that signs requests with a secret key.\n',
    'author': 'Nom Nom Data Inc',
    'author_email': 'info@nomnomdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/nomnomdata/tools/nomnomdata-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.saya',
 'graia.saya.behaviour',
 'graia.saya.builtins',
 'graia.saya.builtins.broadcast']

package_data = \
{'': ['*']}

install_requires = \
['graia-broadcast>=0.7.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'graia-saya',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': '31543961+GreyElaina@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

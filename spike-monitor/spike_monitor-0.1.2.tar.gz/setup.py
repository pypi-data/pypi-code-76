# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spike_monitor']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-logging>=2.2.0,<2.3.0',
 'pendulum>=2.1.2,<2.2.0',
 'pickle4>=0.0.1,<0.1.0',
 'pydantic>=1.7.3,<1.8.0']

setup_kwargs = {
    'name': 'spike-monitor',
    'version': '0.1.2',
    'description': 'This package contains the necessary tools to monitor models',
    'long_description': None,
    'author': 'NicolasITC',
    'author_email': 'n.treimun14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SpikeLab-CL/spk-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)

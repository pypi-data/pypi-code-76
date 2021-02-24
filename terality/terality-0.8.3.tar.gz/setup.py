# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terality',
 'terality._terality',
 'terality._terality.serialization',
 'terality._terality.terality_structures',
 'terality._terality.utils']

package_data = \
{'': ['*']}

install_requires = \
['aioboto3>=8.2.0,<9.0.0',
 'aiobotocore>=1.1,<2.0',
 'dill>=0.3.2,<0.4.0',
 'numpy>=1.18,<2.0',
 'pandas>=1.2.0,<2.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'terality',
    'version': '0.8.3',
    'description': 'The Data Processing Engine for Data Scientists',
    'long_description': "# Terality\n\nTerality is a data processing engine for data scientists. \n\n**Note:** You will need a Terality account to use this package. Contact us on [terality.com](https://www.terality.com/) to get started!\n\n## Setup\n\nConfigure your credentials once and for all by calling the `configure` function:\n\n```python\nimport terality\nterality.configure('<YOUR_USER_ID>', '<YOUR_USER_SECRET>')\n```\n\nBy default, the configuration is written inside a `.terality` directory under the current user's home. You can customize that location through the `TERALITY_HOME` environment variable.\n",
    'author': 'Terality Engineering Team',
    'author_email': 'dev.null@terality.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://terality.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

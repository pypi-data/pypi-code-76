# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic', 'platonic.queue', 'platonic.timeout']

package_data = \
{'': ['*']}

install_requires = \
['typecasts>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'platonic',
    'version': '1.2.0',
    'description': 'Abstract datastructures for Clean Architecture applications in Python.',
    'long_description': '# platonic\n\n[![Build Status](https://travis-ci.com/python-platonic/platonic.svg?branch=master)](https://travis-ci.com/python-platonic/platonic)\n[![Coverage](https://coveralls.io/repos/github/python-platonic/platonic/badge.svg?branch=master)](https://coveralls.io/github/python-platonic/platonic?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/platonic.svg)](https://pypi.org/project/platonic/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n![PyPI - License](https://img.shields.io/pypi/l/platonic)\n\nAbstract data structures for Clean Architecture applications in Python. Amazon services, brokers, and backends represented as queues, mappings, lists, iterables, and more.\n\n## Example \n\n```python\n# TODO\n```\n\n\n# Available data structures\n\n|                 | queue | iterable | dict | list | set | graph |\n| ---             | ---   | ---      | ---  | ---  | --- | ---   |\n| Amazon DynamoDB | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| Amazon SimpleDB | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| Amazon SQS      | ✔    ️| 🔧       | ❌    | 🔧   | 🔧  | 🔧    |\n| Amazon S3       | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| Apache Kafka    | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| Local FS        | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| MongoDB         | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| MySQL           | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| OrientDB        | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| PostgreSQL      | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n| Redis           | 🔧    | 🔧       | 🔧   | 🔧   | 🔧  | 🔧    |\n\n\n## Installation\n\n```bash\npip install platonic\n```\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [3cb37d9e138d83958c4d915a3b3aa737b27b6418](https://github.com/wemake-services/wemake-python-package/tree/3cb37d9e138d83958c4d915a3b3aa737b27b6418). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/3cb37d9e138d83958c4d915a3b3aa737b27b6418...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-platonic/platonic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic', 'platonic.sqs', 'platonic.sqs.queue']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'boltons>=20.2.1,<21.0.0',
 'boto3-stubs[sqs]>=1.15.10,<2.0.0',
 'platonic>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'platonic-sqs',
    'version': '1.2.0',
    'description': 'Platonic wrapper for Amazon Simple Queue Service',
    'long_description': '# platonic.SQS\n\n[![Build Status](https://travis-ci.com/python-platonic/platonic-sqs.svg?branch=master)](https://travis-ci.com/python-platonic/platonic-sqs)\n[![Coverage](https://coveralls.io/repos/github/python-platonic/platonic-sqs/badge.svg?branch=master)](https://coveralls.io/github/python-platonic/platonic-sqs?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/platonic-sqs.svg)](https://pypi.org/project/platonic-sqs/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nPlatonic wrapper for Amazon Simple Queue Service\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install platonic.sqs\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\n...\n```\n\n## License\n\n[MIT](https://github.com/python-platonic/platonic-sqs/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [c9e9ea8b9be2464cacd00b9c2a438e821da9121b](https://github.com/wemake-services/wemake-python-package/tree/c9e9ea8b9be2464cacd00b9c2a438e821da9121b). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/c9e9ea8b9be2464cacd00b9c2a438e821da9121b...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-platonic/platonic-sqs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

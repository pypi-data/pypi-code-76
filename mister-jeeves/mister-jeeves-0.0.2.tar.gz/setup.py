# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeeves', 'jeeves.commands']

package_data = \
{'': ['*']}

install_requires = \
['dependencies>=6.0.1,<7.0.0',
 'flakehell>=0.9.0,<0.10.0',
 'isort>=5.7.0,<6.0.0',
 'typer>=0.3.2,<0.4.0',
 'wemake-python-styleguide>=0.15.1,<0.16.0']

entry_points = \
{'console_scripts': ['jeeves = jeeves.cli:app']}

setup_kwargs = {
    'name': 'mister-jeeves',
    'version': '0.0.2',
    'description': 'Mr Jeeves will be happy to help you managing your Python project sir.',
    'long_description': '# jeeves\n\n[![Build Status](https://github.com/python-jeeves/jeeves/workflows/test/badge.svg?branch=master&event=push)](https://github.com/python-jeeves/jeeves/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/python-jeeves/jeeves/branch/master/graph/badge.svg)](https://codecov.io/gh/python-jeeves/jeeves)\n[![Python Version](https://img.shields.io/pypi/pyversions/jeeves.svg)](https://pypi.org/project/jeeves/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nMr Jeeves will be happy to help you managing your Python project sir.\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install jeeves\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom jeeves.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[MIT](https://github.com/python-jeeves/jeeves/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [06dd6b090ca018c0a07b1ad6c889e14951925b77](https://github.com/wemake-services/wemake-python-package/tree/06dd6b090ca018c0a07b1ad6c889e14951925b77). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/06dd6b090ca018c0a07b1ad6c889e14951925b77...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-jeeves/jeeves',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)

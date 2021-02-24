# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkgs_rissangs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pypkgs-rissangs',
    'version': '1.1.5',
    'description': 'Python package that eases the pain of concatenating Pandas categoricals.',
    'long_description': '# pypkgs_rissangs \n\n![](https://github.com/rissangs/pypkgs_rissangs/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/rissangs/pypkgs_rissangs/branch/main/graph/badge.svg)](https://codecov.io/gh/rissangs/pypkgs_rissangs) ![Release](https://github.com/rissangs/pypkgs_rissangs/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pypkgs_rissangs/badge/?version=latest)](https://pypkgs_rissangs.readthedocs.io/en/latest/?badge=latest)\n\nPython package that eases the pain of concatenating Pandas categoricals\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ pypkgs_rissangs\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://pypkgs_rissangs.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/rissangs/pypkgs_rissangs/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'rissangs',
    'author_email': '70673560+rissangs@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

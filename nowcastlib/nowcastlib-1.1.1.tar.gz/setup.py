# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nowcastlib']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.18.5', 'pandas==1.1.5']

setup_kwargs = {
    'name': 'nowcastlib',
    'version': '1.1.1',
    'description': '🧙🔧 Utils that can be reused and shared across and beyond the ESO Nowcast project',
    'long_description': '# Nowcast Library\n\n🧙\u200d♂️🔧 Utils that can be reused and shared across and beyond the Nowcast project\n\n## Installation\n\nSimply run\n\n```console\npip install nowcastlib\n```\n\n## Development Setup\n\nThis repository relies on [Poetry](https://python-poetry.org/) for tracking\ndependencies, building and publishing. It is therefore recommended that\ndevelopers [install poetry](https://python-poetry.org/docs/#installation) and\nmake use of it throughout their development of the project.\n\n### Dependencies\n\nMake sure you are in the right Python environment and run\n\n```console\npoetry install\n```\n\nThis reads [pyproject.toml](./pyproject.toml), resolves the dependencies, and\ninstalls them.\n\n### Deployment\n\nThe repository is published to [PyPi](https://pypi.org/), so to make it\naccessible via a `pip install` command as mentioned [earlier](#install).\n\nTo publish changes follow these steps:\n\n1. Changes should be merged into the master branch. Ideally this process is\n   automated via a CI tool.\n2. Optionally run\n   [`poetry version`](https://python-poetry.org/docs/cli/#version) with the\n   appropriate argument based on [semver guidelines](https://semver.org/).\n3. Prepare the package by running\n\n   ```console\n   poetry build\n   ```\n\n4. Ensure you have [TestPyPi](https://test.pypi.org/) and PyPi configured as\n   your poetry repositories:\n\n   ```console\n   > poetry config repositories.testpypi https://test.pypi.org/legacy/\n\n   > poetry config repositories.pypi https://pypi.org/\n\n   > poetry config --list\n   repositories.pypi.url = "https://pypi.org/"\n   repositories.testpypi.url = "https://test.pypi.org/legacy/"\n   ```\n\n5. Publish the repository to TestPyPi, to see that everything works as expected:\n\n   ```console\n   poetry publish -r testpypi\n   ```\n\n6. Publish the repository to PyPi:\n\n   ```console\n   poetry publish -r pypi\n   ```\n',
    'author': 'Giulio Starace',
    'author_email': 'giulio.starace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.eso.org/gstarace/nowcast-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)

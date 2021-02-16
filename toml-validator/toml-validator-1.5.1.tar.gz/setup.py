# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['toml_validator', 'toml_validator.use_cases']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'tomlkit>=0.5.9,<0.8.0']

entry_points = \
{'console_scripts': ['toml-validator = toml_validator.__main__:main']}

setup_kwargs = {
    'name': 'toml-validator',
    'version': '1.5.1',
    'description': 'Simple TOML file validator using Python.',
    'long_description': "TOML Validator\n==============\n\n**MAINTAINER NEEDED: this project is complete but won't be updated until further notice. If you have interest in improving it, please contact me by creating an** `issue here`_ **.**\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/toml-validator.svg\n   :target: https://pypi.org/project/toml-validator/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/toml-validator\n   :target: https://pypi.org/project/toml-validator\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/toml-validator\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/toml-validator/latest.svg?label=Read%20the%20Docs\n   :target: https://toml-validator.readthedocs.io/\n   :alt: Read the documentation at https://toml-validator.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/toml-validator/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/toml-validator/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/toml-validator/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/toml-validator\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\nCLI for tomlkit_.\n\n\nRequirements\n------------\n\nYou need Python 3.7.0 or above (latest 3.9 recommended) installed on your machine.\n\n\nInstallation\n------------\n\nYou can install *TOML Validator* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install toml-validator\n\n\nUsage\n-----\n\n.. code:: console\n\n   $ toml-validator FILAPATH1 FILEPATH2 ...\n\n\nIt gives a green message for correct files and red message with errors.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*TOML Validator* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _issue here: https://github.com/staticdev/staticdev/issues\n.. _tomlkit: https://pypi.org/project/tomlkit\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/staticdev/toml-validator/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/toml-validator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['human_readable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'human-readable',
    'version': '0.2.0',
    'description': 'Human Readable',
    'long_description': 'Human Readable\n==============\n\n|Status| |PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |Status| image:: https://badgen.net/badge/status/alpha/d8624d\n   :target: https://badgen.net/badge/status/alpha/d8624d\n   :alt: Status\n.. |PyPI| image:: https://img.shields.io/pypi/v/human-readable.svg\n   :target: https://pypi.org/project/human-readable/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/human-readable\n   :target: https://pypi.org/project/human-readable\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/human-readable\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/human-readable/latest.svg?label=Read%20the%20Docs\n   :target: https://human-readable.readthedocs.io/\n   :alt: Read the documentation at https://human-readable.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/human-readable/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/human-readable/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/human-readable/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/human-readable\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* File size humanization.\n* List humanization.\n\n\nRequirements\n------------\n\n* It works in Python 3.7+.\n\n\nInstallation\n------------\n\nYou can install *Human Readable* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install human-readable\n\n\nUsage\n-----\n\nImport the lib with:\n\n.. code-block:: python\n\n   import human_readable\n\n\nFile size humanization:\n\n.. code-block:: python\n\n   human_readable.file_size(1000000)\n   "1.0 MB"\n\n   human_readable.file_size(1000000, binary=True)\n   "976.6 KiB"\n\n   human_readable.file_size(1000000, gnu=True)\n   "976.6K"\n\n\nLists humanization:\n\n.. code-block:: python\n\n   human_readable.listing(["Alpha", "Bravo"], ",")\n   "Alpha, Bravo"\n\n   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")\n   "Alpha; Bravo or Charlie"\n\n\nNumbers humanization:\n\n.. code-block:: python\n\n   human_readable.int_comma(12345)\n   "12,345"\n\n   human_readable.int_word(123455913)\n   "123.5 million"\n\n   human_readable.int_word(12345591313)\n   "12.3 billion"\n\n   human_readable.ap_number(4)\n   "four"\n\n   human_readable.ap_number(41)\n   "41"\n\n\nFloating point number humanization:\n\n.. code-block:: python\n\n   human_readable.fractional(1.5)\n   "1 1/2"\n\n   human_readable.fractional(0.3)\n   "3/10"\n\n\nScientific notation:\n\n.. code-block:: python\n\n   human_readable.scientific_notation(1000)\n   "1.00 x 10³"\n\n   human_readable.scientific_notation(5781651000, precision=4)\n   "5.7817 x 10⁹"\n\n\nClick here for more examples and detailed usage_.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Human Readable* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis lib is based on original humanize_ with some added features such as listing, improved naming, documentation, some more testing, bug fixes and better Portuguese support.\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _humanize: https://github.com/jmoiron/humanize\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/staticdev/human-readable/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _usage: https://human-readable.readthedocs.io/en/latest/usage.html\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/human-readable',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

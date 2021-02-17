# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acm_dl_searcher', 'tests']

package_data = \
{'': ['*'], 'acm_dl_searcher': ['templates/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'bibtexparser>=1.2.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'fuzzysearch>=0.7.3,<0.8.0',
 'liquidpy>=0.6.2,<0.7.0',
 'minilog>=1.5,<2.0',
 'requests>=2.24.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.51.0,<5.0.0']

entry_points = \
{'console_scripts': ['acm-dl-searcher = acm_dl_searcher.cli:cli']}

setup_kwargs = {
    'name': 'acm-dl-searcher',
    'version': '0.1.0a3',
    'description': 'Top-level package for ACM DL Searcher.',
    'long_description': '===================\nACM DL Searcher\n===================\n\n\n.. image:: https://img.shields.io/pypi/v/acm_dl_hci_searcher.svg\n        :target: https://pypi.python.org/pypi/acm_dl_hci_searcher\n\n.. image:: https://readthedocs.org/projects/acm-dl-hci-searcher/badge/?version=latest\n        :target: https://acm-dl-hci-searcher.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nA simple command line tool to collect the entries on a particular venue and in acm and run searches on them.\n\n\nInstall\n-------\n\n.. code:: sh\n          \n   pip install acm-dl-searcher\n\nUsage\n--------\nIf getting the entries from the `CHI 16`_ Conference:\n\n* To get the entries of a particular venue:\n\n  .. code:: sh\n\n            acm-dl-searcher get 10.1145/2858036 --short-name "CHI 16""\n  \n  This will download all the entries and their abstracts. The short-name provided can be anything. The first parameter expected for ``amc-dl-searcher get`` is the doi of the venue.\n\n* To list all the venues saved:\n\n  .. code:: sh\n\n            acm-dl-searcher list\n\n* To search the from the saved venues:\n\n  .. code:: sh\n\n            acm-dl-searcher search "adaptive"\n\n  This will search all the venues obtained through ``acm-dl-searcher get``, and list out the paper and titles that contain the phrase "adaptive" in the abstract or title. Currently the searcher uses a fuzzy search with a maximum difference of 2.\n\n  To narrow the search to particular venue(s) use the option ``--venue-short-name-filter``:\n\n  .. code:: sh\n\n            acm-dl-searcher search "adaptive" --venue-short-name-filter "CHI"\n\n  This will list out the matches from venues whose `short name` contain "CHI".\n\n  To print out the abstracts as well use the option ``--print-abstracts``:\n  \n  .. code:: sh\n            \n     acm-dl-searcher search "adaptive" --print-abstracts\n\n  To view the results on the browser use the option ``--html``:\n  \n  .. code:: sh\n            \n     acm-dl-searcher search "adaptive" --html\n\n  \n\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n.. _`CHI 16`: https://dl.acm.org/doi/proceedings/10.1145/2858036\n',
    'author': 'Ahmed Shariff',
    'author_email': 'shariff.mfa@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahmed-shariff/acm_dl_searcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

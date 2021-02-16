# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autograde', 'autograde.cli', 'autograde.static']

package_data = \
{'': ['*'], 'autograde': ['templates/*']}

install_requires = \
['Flask>=1.1,<1.2',
 'Jinja2>=2.11,<2.12',
 'dataclasses-json>=0.5,<0.6',
 'django-htmlmin-ajax>=0.11,<0.12',
 'ipykernel>=5.4,<5.5',
 'jupyter>=1.0,<1.1',
 'matplotlib>=3.3,<3.4',
 'numpy>=1.20,<1.21',
 'pandas>=1.2,<1.3',
 'scipy>=1.6,<1.7',
 'seaborn>=0.11,<0.12']

entry_points = \
{'console_scripts': ['autograde = autograde.cli.__main__:cli']}

setup_kwargs = {
    'name': 'jupyter-autograde',
    'version': '0.2.7',
    'description': 'Unittesting & Grading of Jupyter Notebooks',
    'long_description': ".. _auto-grade:\n\n=========\nautograde\n=========\n\n.. image:: https://github.com/cssh-rwth/autograde/workflows/test%20autograde/badge.svg\n   :alt: autograde test\n   :target: https://github.com/cssh-rwth/autograde/actions\n\n.. image:: https://img.shields.io/pypi/v/jupyter-autograde?color=blue&label=jupyter-autograde\n   :alt: autograde on PyPI\n   :target: https://pypi.org/project/jupyter-autograde\n\n*autograde* is a tool for testing *Jupyter* notebooks. Its features include execution of notebooks (optionally isolated via docker/podman) with consecutive unit testing of the final notebook state. On top of that, an audit mode allows for refining results (e.g. grading plots by hand). Eventually, *autograde* can summarize these results in human and machine readable formats.\n\nsetup\n-----\n\nBefore installing *autograde* and in case you want to use it with a container backend, ensure `docker <https://www.docker.com/>`_ **or** `podman <https://podman.io/>`_ is available on your system.\nWe recommend podman as it runs rootless.\n\nNow, in order to install *autograde*, run :code:`pip install jupyter-autograde`.\nAlternatively, you can install *autograde* from source by cloning this repository and runing :code:`poetry install` within it.\nThis requires `poetry <https://python-poetry.org/docs/>`_ to be installed on your system!\n\nEventually, build the respective container image: :code:`python -m autograde build`.\n**Note:** in order to build a container image, *autograde* must not be installed via *PyPI* but from source code!\n\nusage\n-----\n\ntesting\n```````\n\n*autograde* comes with some example files located in the :code:`demo/` subdirectory that we will use for now to illustrate the workflow. Run:\n\n::\n\n    python -m autograde test demo/test.py demo/notebook.ipynb --target /tmp --context demo/context\n\nWhat happened? Let's first have a look at the arguments of *autograde*:\n\n* :code:`demo/test.py` a script with test cases we want apply\n* :code:`demo/notebook.ipynb` is the a notebook to be tested (here you may also specify a directory to be recursively searched for notebooks)\n* The optional flag :code:`--target` tells *autograde* where to store results, :code:`/tmp` in our case, and the current working directory by default.\n* The optional flag :code:`--context` specifies a directory that is mounted into the sandbox and may contain arbitrary files or subdirectories.\n  This is useful when the notebook expects some external files to be present such as data sets.\n\nThe output is a compressed archive that is named something like :code:`results_[Lastname1,Lastname2,...]_XXXXXXXX.zip` and which has the following contents:\n\n* :code:`artifacts/`: directory with all files that where created or modified by the tested notebook as well as rendered matplotlib plots.\n* :code:`code.py`: code extracted from the notebook including :code:`stdout`/:code:`stderr` as comments\n* :code:`notebook.ipynb`: an identical copy of the tested notebook\n* :code:`test_restults.json`: test results\n\n\nreports\n```````\n\nThe :code:`report` sub command creates human readable HTML reports from test results:\n\n::\n\n    python -m autograde report path/to/result(s)\n\nThe respective report is added to the results archive inplace.\n\n\npatching\n````````\n\nResults from multiple test runs can be merged via the :code:`patch` sub command:\n\n::\n\n    python -m autograde patch path/to/result(s) /path/to/patch/result(s)\n\n\nsummarize results\n`````````````````\n\nIn a typical scenario, test cases are not just applied to one notebook but many at a time.\nTherefore, *autograde* comes with a summary feature, that aggregates results, shows you a score distribution and has some very basic fraud detection.\nTo create a summary, simply run:\n\n::\n\n    python -m autograde summary path/to/results\n\nTwo new files will appear in the result directory:\n\n* :code:`summary.csv`: aggregated results\n* :code:`summary.html`: human readable summary report\n\n\nhelp\n````\n\nTo get an overview of all available commands and their usage, run\n\n::\n\n    python -m autograde [sub command] --help\n\n",
    'author': 'Lukas Ochse',
    'author_email': None,
    'maintainer': 'Chair for Computational Social Sciences and Humanities at RWTH Aachen University',
    'maintainer_email': None,
    'url': 'https://github.com/cssh-rwth/autograde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

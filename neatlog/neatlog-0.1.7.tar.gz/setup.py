# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neatlog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'neatlog',
    'version': '0.1.7',
    'description': 'A neat logging configurator',
    'long_description': '.. image:: https://img.shields.io/pypi/v/neatlog?style=flat-square\n   :target: https://pypi.org/project/neatlog/\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/l/neatlog?style=flat-square\n   :target: https://gitlab.com/szs/neatlog/-/raw/master/LICENSE\n   :alt: PyPI - License\n\n.. image:: https://img.shields.io/pypi/pyversions/neatlog?style=flat-square\n   :target: https://python.org\n   :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/gitlab/pipeline/szs/neatlog?style=flat-square\n   :target: https://gitlab.com/szs/neatlog/-/pipelines\n   :alt: Gitlab pipeline status\n\n.. image:: https://gitlab.com/szs/neatlog/badges/master/coverage.svg?style=flat-square\n   :target: https://gitlab.com/szs/neatlog/-/pipelines\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/neatlog/badge/?version=latest\n   :target: https://neatlog.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n\nneatlog: A neat logging configuration\n=====================================\n\nThis package provides an easy and transparent way of customizing the builtin logging.\nJust import the module and enjoy the difference.\n\nInstallation\n============\n\nThe installation is straight forward. You can install the package via ``pip``, ``pipenv``, ``poetry``\nand alike or by downloading the source from the gitlab repository.\n\nFrom pypi.org (recommended)\n---------------------------\n\nInstall by typing\n\n.. code-block:: shell\n\n                pip install neatlog\n\nor\n\n.. code-block:: shell\n\n                pip install --user neatlog\n\nif you do not have root access.\n\nPlease check the documentations for `pipenv <https://pipenv.pypa.io/en/latest/>`_, and\n`poetry <https://python-poetry.org/docs/>`_ for information on how to install packages with these tools.\n\nFrom gitlab.com (for experts)\n-----------------------------\n\nTo get the latest features or contribute to the development, you can clone the whole project using\n`git <https://git-scm.com/>`_:\n\n.. code-block:: shell\n\n                git clone https://gitlab.com/szs/neatlog.git\n\n\nUsage\n=====\n\nSimply import neatlog in your program and use logging as usually:\n\n.. code-block:: python\n\n                import logging\n                from log_fmt import set_log_level\n\n                set_log_level(logging.DEBUG)\n                logging.critical("something critical")\n                logging.error("some error")\n                logging.warning("some warning")\n                logging.info("some info")\n                logging.debug("something for debugging")\n\nHow to Contribute\n=================\n\nIf you find a bug, want to propose a feature or need help getting this package to work with your data\non your system, please don\'t hesitate to file an `issue <https://gitlab.com/szs/neatlog/-/issues>`_ or write\nan email. Merge requests are also much appreciated!\n\nProject links\n=============\n\n* `Repository <https://gitlab.com/szs/neatlog>`_\n* `Documentation <https://neatlog.readthedocs.io/en/latest/>`_\n* `pypi page <https://pypi.org/project/neatlog/>`_\n',
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/szs/neatlog/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

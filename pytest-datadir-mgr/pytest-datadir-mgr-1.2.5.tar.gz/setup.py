# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_datadir_mgr']

package_data = \
{'': ['*']}

install_requires = \
['progressbar2>=3.52.1,<4.0.0',
 'pytest>=6.0.1,<7.0.0',
 'requests_download>=0.1.2,<0.2.0']

entry_points = \
{'pytest11': ['datadir_mgr = pytest_datadir_mgr']}

setup_kwargs = {
    'name': 'pytest-datadir-mgr',
    'version': '1.2.5',
    'description': 'Manager for test data providing downloads, caching of generated files, and a context for temp directories.',
    'long_description': 'datadir-mgr plugin for pytest\n=============================\n\nThe ``datadir-mgr`` plugin for pytest_ provides the ``datadir_mgr`` fixture which\nallow test functions to easily download data files and cache generated data files\nin data directories in a manner that allows for overlaying of results. ``datadir-mgr``\nis pathlib-based, so complete paths to data files are handled,\nnot just filenames.\n\n\n\nThe ``datadir_mgr`` behaves like a limited dictionary, with ``datadir_mgr[item]`` returning a path with the\nmost specific scope (out of ``global, module, [class], [function]`` that matches the string or path specified\nby ``item``.  In addition to serving data files already stored in the data directory, the fixture provides\nfive methods useful for adding to the test data stored in the repository:\n\n- The ``download`` method allows downloading data files into data directories, with\n  option MD5 checksum checks, un-gzipping, and a progressbar.\n- The ``savepath`` fixture lets an arbitrary path relative to the current working\n  directory to be saved at a particular scope in the data directories.\n- The ``add_scope`` method lets one add directories from scopes different from\n  the present request to be added to the search path.  This lets the results\n  of previous cached steps to be used in scopes other than global.\n- The ``in_tmp_dir`` method creates a context in a temporary directory with\n  a list of request file paths copied in.  Optionally, all output file paths\n  can be saved at a particular scope at cleanup with an optional exclusion\n  filter pattern (e.g., for excluding log files).  Note that files in directories\n  that begin with ``test_`` or end with ``_test`` could be confused with\n  scope directories and cannnot be saved.  If ``progressbar`` is set to "True",\n  then the progress of file copying will be shown, which is helpful in some long-running\n  pytest jobs, e.g. on Travis.\n- The ``paths_from_scope`` returns a list of all paths to files from a specified scope.\n\n\nPrerequisites\n-------------\nPython 3.6 or greater is required.\nThis package is tested under Linux and MacOS using Python 3.8.\n\nInstallation for Users\n----------------------\nInstall via pip ::\n\n     pip install pytest-datadir-mgr\n\nFor Developers\n--------------\nIf you plan to develop ``datadir_mgr``, you\'ll need to install\nthe `poetry <https://python-poetry.org>`_ dependency manager.\nIf you haven\'t previously installed ``poetry``, execute the command: ::\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nNext, get the master branch from GitHub ::\n\n\tgit clone https://github.com/joelb123/pytest-datadir-mgr.git\n\nChange to the ``datadir-mgr/`` directory and install with poetry: ::\n\n\tpoetry install -v\n\nTest ``datadir-mgr`` with ``poetry``: ::\n\n    poetry run pytest -s\n\nProject Status\n--------------\n+-------------------+-------------+\n| Latest Release    | |pypi|      |\n+-------------------+-------------+\n| Activity          | |downloads| |\n+-------------------+-------------+\n| License           | |license|   |\n+-------------------+-------------+\n| Build             | |build|     |\n+-------------------+-------------+\n| Coverage          | |coverage|  |\n+-------------------+-------------+\n| Code Grade        | |codacy|    |\n+-------------------+-------------+\n| Issues            | |issues|    |\n+-------------------+-------------+\n\n.. _pytest: http://pytest.org/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pytest-datadir-mgr.svg\n    :target: https://pypi.python.org/pypi/pytest-datadir-mgr\n    :alt: Python package\n\n.. |repo| image:: https://img.shields.io/github/commits-since/joelb123/pytest-datadir-mgr/0.1.0.svg\n    :target: https://github.com/joelb123/pytest-datadir-mgr\n    :alt: GitHub repository\n\n.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n    :target: https://github.com/joelb123/pytest-datadir-mgr/blob/master/LICENSE.txt\n    :alt: License terms\n\n.. |build| image:: https://github.com/joelb123/pytest-datadir-mgr/workflows/tests/badge.svg\n    :target:  https://github.com/joelb123/pytest-datadir-mgr.actions\n    :alt: GitHub Actions\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/f306c40d604f4e62b8731ada896d8eb2\n    :target: https://www.codacy.com/gh/joelb123/pytest-datadir-mgr?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joelb123/pytest-datadir-mgr&amp;utm_campaign=Badge_Grade\n    :alt: Codacy.io grade\n\n.. |coverage| image:: https://codecov.io/gh/joelb123/pytest-datadir-mgr/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/joelb123/pytest-datadir-mgr\n    :alt: Codecov.io test coverage\n\n.. |issues| image:: https://img.shields.io/github/issues/joelb123/pytest-datadir-mgr.svg\n    :target:  https://github.com/joelb123/pytest-datadir-mgr/issues\n    :alt: Issues reported\n\n.. |downloads| image:: https://pepy.tech/badge/pytest_datadir_mgr\n     :target: https://pepy.tech/project/pytest_datadir_mgr\n     :alt: Download stats\n',
    'author': 'Joel Berendzen',
    'author_email': 'joelb@generisbio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joelb123/pytest-datadir-mgr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

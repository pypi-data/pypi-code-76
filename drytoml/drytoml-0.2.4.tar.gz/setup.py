# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drytoml', 'drytoml.app']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'tomlkit>=0.7.0,<0.8.0']

extras_require = \
{'all': ['black>=20.8b1,<21.0',
         'flakeheaven>=0.10.0-alpha.0,<0.11.0',
         'isort>=5.7.0,<6.0.0'],
 'black': ['black>=20.8b1,<21.0'],
 'dev': ['black>=20.8b1,<21.0',
         'flakeheaven>=0.10.0-alpha.0,<0.11.0',
         'isort>=5.7.0,<6.0.0',
         'pytest>=6.2.2,<7.0.0',
         'Sphinx>=3.4.3,<4.0.0',
         'pytest-cov>=2.11.1,<3.0.0',
         'sphinx-rtd-theme>=0.5.1,<0.6.0',
         'flake8-bandit>=2.1.2,<3.0.0',
         'flake8-bugbear>=20.11.1,<21.0.0',
         'flake8-builtins>=1.5.3,<2.0.0',
         'flake8-comprehensions>=3.3.1,<4.0.0',
         'darglint>=1.6.0,<2.0.0',
         'flake8-docstrings>=1.5.0,<2.0.0',
         'flake8-eradicate>=1.0.0,<2.0.0',
         'flake8-mutable>=1.2.0,<2.0.0',
         'flake8-debugger>=4.0.0,<5.0.0',
         'flake8-pytest-style>=1.3.0,<2.0.0',
         'pep8-naming>=0.11.1,<0.12.0',
         'pytest-html>=3.1.1,<4.0.0',
         'm2r2>=0.2.7,<0.3.0',
         'recommonmark>=0.7.1,<0.8.0',
         'commitizen>=2.14.2,<3.0.0',
         'pre-commit>=2.10.1,<3.0.0',
         'pylint>=2.6.0,<3.0.0'],
 'docs': ['Sphinx>=3.4.3,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'm2r2>=0.2.7,<0.3.0',
          'recommonmark>=0.7.1,<0.8.0'],
 'flakehell': ['flakeheaven>=0.10.0-alpha.0,<0.11.0'],
 'format': ['black>=20.8b1,<21.0', 'isort>=5.7.0,<6.0.0'],
 'isort': ['isort>=5.7.0,<6.0.0'],
 'lint': ['black>=20.8b1,<21.0',
          'flakeheaven>=0.10.0-alpha.0,<0.11.0',
          'isort>=5.7.0,<6.0.0',
          'pytest>=6.2.2,<7.0.0',
          'flake8-bandit>=2.1.2,<3.0.0',
          'flake8-bugbear>=20.11.1,<21.0.0',
          'flake8-builtins>=1.5.3,<2.0.0',
          'flake8-comprehensions>=3.3.1,<4.0.0',
          'darglint>=1.6.0,<2.0.0',
          'flake8-docstrings>=1.5.0,<2.0.0',
          'flake8-eradicate>=1.0.0,<2.0.0',
          'flake8-mutable>=1.2.0,<2.0.0',
          'flake8-debugger>=4.0.0,<5.0.0',
          'flake8-pytest-style>=1.3.0,<2.0.0',
          'pep8-naming>=0.11.1,<0.12.0',
          'pylint>=2.6.0,<3.0.0'],
 'test': ['pytest>=6.2.2,<7.0.0',
          'pytest-cov>=2.11.1,<3.0.0',
          'pytest-html>=3.1.1,<4.0.0']}

entry_points = \
{'console_scripts': ['dry = drytoml.app:main']}

setup_kwargs = {
    'name': 'drytoml',
    'version': '0.2.4',
    'description': 'Keep toml configuration centralized and personalizable',
    'long_description': '# drytoml\n\nKeep your toml configuration centralized and personalizable.\n\n---\n\n[![PyPI](https://img.shields.io/pypi/v/drytoml?color=yellow)](https://pypi.org/project/drytoml/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/drytoml)](https://www.python.org/downloads/)\n\n---\n\n[![ReadTheDocs](https://readthedocs.org/projects/drytoml/badge/?version=latest)](https://drytoml.readthedocs.io/en/latest/)\n\n---\n\n[![Format](https://github.com/pwoolvett/drytoml/workflows/Format/badge.svg)](https://github.com/pwoolvett/drytoml/actions?query=workflow%3AFormat)\n[![Lint](https://github.com/pwoolvett/drytoml/workflows/Lint/badge.svg)](https://github.com/pwoolvett/drytoml/actions?query=workflow%3ALint)\n[![Test](https://github.com/pwoolvett/drytoml/workflows/Test/badge.svg)](https://github.com/pwoolvett/drytoml/actions?query=workflow%3ATest)\n[![codecov](https://codecov.io/gh/pwoolvett/drytoml/branch/master/graph/badge.svg?token=YXO8NDUU0G)](https://codecov.io/gh/pwoolvett/drytoml)\n\n---\n\n[![VSCode Ready-to-Code](https://img.shields.io/badge/devcontainer-enabled-blue?logo=docker)](https://code.visualstudio.com/docs/remote/containers)\n[![License: Unlicense](https://img.shields.io/badge/license-UNLICENSE-white.svg)](http://unlicense.org/)\n\n\n---\n\n\nThrough `drytoml`, TOML files can have references to any content from another TOML file.\nReferences work with relative/absolute paths and urls, and can point to whole files, a\nspecific table, or in general anything reachable by a sequence of `getitem` calls, like\n`["tool", "poetry", "source", 0, "url"]`. `drytoml` takes care of transcluding the\ncontent for you.\n\nInspired by [flakehell](https://pypi.org/project/flakehell/) and\n[nitpick](https://pypi.org/project/nitpick/), the main motivation behind `drytoml` is to\nhave several projects sharing a common, centralized configuration defining codestyles,\nbut still allowing granular control when required.\n\nThis is a deliberate departure from [nitpick](https://pypi.org/project/nitpick/), which\nworks as a linter instead, ensuring your local files have the right content.\n\n\n## Usage\n\n`drytoml` has two main usages:\n\n1. Use a file as a reference and "build" the resulting one:\n\n    ```toml\n    # contents of pyproject.dry.toml\n    ...\n    [tool.black]\n    __extends = "../../common/black.toml"\n    target-version = [\'py37\']\n    include = \'\\.pyi?$\'\n    ...\n    ```\n\n    ```toml\n    # contents of ../../common/black.toml\n    [tool.black]\n    line-length = 100\n    ```\n\n   ```console\n   $ dry export --file=pyproject.dry.toml > pyproject.toml\n   ```\n\n    ```toml\n    # contents of pyproject.toml\n    [tool.black]\n    line-length = 100\n    target-version = [\'py37\']\n    include = \'\\.pyi?$\'\n    ```\n\n2. Use included wrappers, allowing you to use references in your current configuration\n   without changing any file:\n\n   Consider the original `pyproject.dry.toml` from the example above, an alternative\n   usage for `drytoml` is shown next. Instead of this:\n\n   ```console\n   $ black .\n   All done! ✨ 🍰 ✨\n   14 files left unchanged.\n   ```\n\n   You would run this:\n\n   ```console\n   $ dry black\n   reformatted /path/to/cwd/file_with_potentially_long_lines.py\n   reformatted /path/to/cwd/another_file_with_potentially_long_lines.py\n   All done! ✨ 🍰 ✨\n   2 files reformatted, 12 files left unchanged.\n   ```\n\n   What just happened? `drytoml` comes with a set of wrappers which\n\n   1. Create a transcluded temporary file, equivalent to the resulting `pyproject.toml`\n      in the example above\n   2. Configure the wrapped tool (`black` in this case) to use the temporary file\n   3. Run `black`, and get rid of the file on exit.\n\n\nFor the moment, the following wrappers are available (more to come, contributions are\nwelcome):\n\n* [x] [black](https://github.com/psf/black)\n* [x] [isort](https://pycqa.github.io/isort/)\n* [x] [flakehell, flake8helled](https://github.com/life4/flakehell) *\n\nIn the works:\n* [ ] docformatter\n* [ ] pytest\n\n### Notes\n\nAlthough the flakehell project was archived, we\'re keeping a fork alive from\n[here](https://github.com/pwoolvett/flakehell), availabe as\n[flakeheaven](https://pypi.org/project/flakeheaven) in pypi.\n\n\n## Setup\n\n### Prerequisites\n\n  * A compatible python >3.6.9\n  * [recommended] virtualenv\n  * A recent `pip`\n\n### Install\n\n  Install as usual, with `pip`, `poetry`, etc:\n\n* `pip install drytoml`\n* `poetry add drytoml` (probably you\'ll want `poetry add --dev drytoml` instead)\n\n## Usage\n\nFor any command , run `--help` to find out flags and usage.\nSome of the most common are listed below:\n\n* Use any of the provided wrappers as a subcommand, eg `dry black` instead of `black`.\n* Use `dry -q export` and redirect to a file, to generate a new file with transcluded\n  contents\n* Use `dry cache` to manage the cache for remote references.\n\n\n\n## FAQ\n\n**Q: I want to use a different key to trigger transclusions**\n\n   A: In cli mode (using the `dry` command), you can pass the `--key` flagcli, to change\n   it. In api mode (from python code), initialize `drytoml.parser.Parser` using a\n   custom value for the `extend_key` kwarg.\n\n\n**Q: I changed a referenced toml upstream (eg in github) but still get the same result.**\n\n   A: Run `dry cache clear --help` to see available options.\n\n## Contribute\n\nStart by creating an issue, forking the project and creating a Pull Request.\n\n### Setting up the development environment\n\nIf you have docker, the easiest way is to use the provided devcontainer inside vscode,\nwhich already contains everything pre-installed. You must open the cloned directory\nusing the [remote-containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).\nJust run `poetry shell` or prepend any command with `poetry run` to ensure commands\nare run inside the virtual environment.\n\nAlternatively, you can use poetry: `poetry install -E dev`\n\nThe next steps assume you have already activated the venv.\n\n### Committing\n\n* Commits in every branch must adhere to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).\n  Releases are done automatically and require conventional commits messages compliance.\n\n* To validate commits, you can install the pre-commit hook\n\n  ```console\n  pre-commit install --hook-type commit-msg\n  ```\n\n* With venv activated, you can commit using `cz commit` instead of `git commit` to\n  ensure compliance.\n\n### Running checks\n\nYou can look at the different actions defined in `.github/workflows`. There are three\nways to check your code:\n\n* Remotely, by pushing to an open PR. You\'ll se the results in the PR page.\n\n* Manually, executing the check from inside a venv\n\n  For example, to generate the documentation, check `.github/workflows/docs`. To run the\n  `Build with Sphinx` step:\n\n  ```console\n  sphinx-build docs/src docs/build\n  ```\n\n  Or to run pytest, from `.github/workflows/tests.yml`:\n\n  ```console\n  sphinx-build docs/src docs/build\n  ```\n\n  ... etc\n\n* Locally, with [act](https://github.com/nektos/act) (Already installed in the\n  devcontainer)\n\nFor example, to emulate a PR run for the tests workflow:\n  \n ```console\n act -W .github/workflows/tests.yml pull_request\n ```\n\n## TODO\n\nCheck out current development [here](https://github.com/pwoolvett/drytoml/projects/2)\n',
    'author': 'Pablo Woolvett',
    'author_email': 'pablowoolvett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwoolvett/drytoml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)

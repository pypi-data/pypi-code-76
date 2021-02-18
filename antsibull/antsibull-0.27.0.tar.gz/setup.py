# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antsibull',
 'antsibull.cli',
 'antsibull.cli.doc_commands',
 'antsibull.data',
 'antsibull.data.docsite',
 'antsibull.docs_parsing',
 'antsibull.jinja2',
 'antsibull.schemas',
 'antsibull.utils',
 'antsibull.vendored',
 'sphinx_antsibull_ext',
 'tests',
 'tests.functional.schema',
 'tests.sphinx',
 'tests.units']

package_data = \
{'': ['*'],
 'antsibull.data': ['debian/*'],
 'sphinx_antsibull_ext': ['css/*'],
 'tests.functional.schema': ['good_data/*']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp>=3.0.0',
 'antsibull-changelog>=0.7.0',
 'asyncio-pool',
 'docutils',
 'jinja2',
 'packaging>=20.0',
 'perky',
 'pydantic',
 'pygments>=2.6.1',
 'rstcheck>=3,<4',
 'semantic_version',
 'sh',
 'sphinx',
 'twiggy>=0.5.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['aiocontextvars']}

entry_points = \
{'console_scripts': ['antsibull-build = antsibull.cli.antsibull_build:main',
                     'antsibull-docs = antsibull.cli.antsibull_docs:main',
                     'antsibull-lint = antsibull.cli.antsibull_lint:main']}

setup_kwargs = {
    'name': 'antsibull',
    'version': '0.27.0',
    'description': 'Tools for building the Ansible Distribution',
    'long_description': "# antsibull -- Ansible Build Scripts\n[![Python linting badge](https://github.com/ansible-community/antsibull/workflows/Python%20linting/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22Python+linting%22+branch%3Amain)\n[![Python testing badge](https://github.com/ansible-community/antsibull/workflows/Python%20testing/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22Python+testing%22+branch%3Amain)\n[![Build CSS testing badge](https://github.com/ansible-community/antsibull/workflows/Build%20CSS/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22Build+CSS%22+branch%3Amain)\n[![dumb PyPI on GH pages badge](https://github.com/ansible-community/antsibull/workflows/👷%20dumb%20PyPI%20on%20GH%20pages/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull/actions?query=workflow%3A%22👷+dumb+PyPI+on+GH+pages%22+branch%3Amain)\n[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull)](https://codecov.io/gh/ansible-community/antsibull)\n\nTooling for building various things related to Ansible\n\nScripts that are here:\n\n* antsibull-build - Builds Ansible-2.10+ from component collections ([docs](docs/build-ansible.rst))\n* antsibull-docs - Extracts documentation from ansible plugins\n* antsibull-lint - Right now only validates ``changelogs/changelog.yaml`` files ([docs](docs/changelog.yaml-format.md))\n\nThis also includes a [Sphinx extension](https://www.sphinx-doc.org/en/master/) `sphinx_antsibull_ext` which provides a lexer for Ansible output and a minimal CSS file to render the output of `antsibull-docs` correctly.\n\nA related project is [antsibull-changelog](https://pypi.org/project/antsibull-changelog/), which is in its [own repository](https://github.com/ansible-community/antsibull-changelog/).\n\nScripts are created by poetry at build time.  So if you want to run from\na checkout, you'll have to run them under poetry::\n\n    python3 -m pip install poetry\n    poetry install  # Installs dependencies into a virtualenv\n    poetry run antsibull-build --help\n\n.. note:: When installing a package published by poetry, it is best to use\n    pip >= 19.0.  Installing with pip-18.1 and below could create scripts which\n    use pkg_resources which can slow down startup time (in some environments by\n    quite a large amount).\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later.\n\n## Using the Sphinx extension\n\nInclude it in your Sphinx configuration ``conf.py``::\n\n```\n# Add it to 'extensions':\nextensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'notfound.extension', 'sphinx_antsibull_ext']\n```\n\n## Updating the CSS file for the Sphinx extension\n\nThe CSS file [sphinx_antsibull_ext/antsibull-minimal.css](https://github.com/ansible-community/antsibull/blob/main/sphinx_antsibull_ext/antsibull-minimal.css) is built from [sphinx_antsibull_ext/css/antsibull-minimal.scss](https://github.com/ansible-community/antsibull/blob/main/sphinx_antsibull_ext/src/antsibull-minimal.scss) using [SASS](https://sass-lang.com/) and [postcss](https://postcss.org/) using [autoprefixer](https://github.com/postcss/autoprefixer) and [cssnano](https://cssnano.co/).\n\nUse the script `build.sh` in `sphinx_antsibull_ext/css/` to build the `.css` file from the `.scss` file:\n\n```\ncd sphinx_antsibull_ext/css/\n./build-css.sh\n```\n\nFor this to work, you need to make sure that `sassc` and `postcss` are on your path and that the autoprefixer and nanocss modules are installed:\n\n```\n# Debian:\napt-get install sassc\n\n# PostCSS, autoprefixer and cssnano require nodejs/npm:\nnpm install -g autoprefixer cssnano postcss postcss-cli\n```\n\n## Creating a new release:\n\nIf you want to create a new release::\n\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\n    git tag $VERSION_NUMBER\n    git push --tags\n    vim pyproject.toml    # Bump the version number\n    git commit -m 'Update the version number for the next release' pyproject.toml\n    git push\n",
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ansible-community/antsibull',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marko_backlinks',
 'marko_backlinks.adapters',
 'marko_backlinks.adapters.markdown',
 'marko_backlinks.adapters.markdown.marko_ext',
 'marko_backlinks.adapters.references_db',
 'marko_backlinks.common',
 'marko_backlinks.dto',
 'marko_backlinks.entrypoints',
 'marko_backlinks.infrastructure',
 'marko_backlinks.interfaces',
 'marko_backlinks.usecases']

package_data = \
{'': ['*']}

install_requires = \
['marko>=0.10,<1.1',
 'rich>=8,<10',
 'sqlalchemy>=1.3.20,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<4.0']}

entry_points = \
{'console_scripts': ['marko-backlinks = '
                     'marko_backlinks.entrypoints.append_linked_references:app']}

setup_kwargs = {
    'name': 'marko-backlinks',
    'version': '0.3.0',
    'description': 'Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template',
    'long_description': '# marko-backlinks\n\n<div align="center">\n\n[![Build status](https://github.com/jb-delafosse/marko-backlinks/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jb-delafosse/marko-backlinks/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/marko-backlinks.svg)](https://pypi.org/project/marko-backlinks/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jb-delafosse/marko-backlinks/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jb-delafosse/marko-backlinks/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/jb-delafosse/marko-backlinks/releases)\n[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)\n\n</div>\n\n## 🤔 Description\n\nThis project provide a markdown to markdown converter that adds a [Bi-Directional Link](https://maggieappleton.com/bidirectionals)\nSection at the end of each markdown files that is converted.\n\n\nThe project also provide a [pre-commit hook](https://pre-commit.com/) so you can easily integrate it within your own projects easily\n\nIt relies heavily on the [Marko](https://github.com/frostming/marko/tree/master/marko) python package that is the only \nMarkdown Parser with a Markdown Renderer that I know of.\n\n## 💭 Why\n\nI believe a great amount of information can be extracted from collaborative notes if we take time to structure them correctly.\n\nI wanted:\n- To make collaborative notes\n- To organize the notes in a [Roam](https://roamresearch.com/) like manner\n- Everyone to be able to navigate through the notes without installing anything\n- This system to be easily adopted by a software engineering team.\n\nUsing git and this converter as a pre-commit, I can easily do all of this ! 🚀\n\n## 🏃 Getting Started\n<details>\n  <summary>Installation as a python package with pip</summary>\n\nConsidering you already have python available. You can simply add th\n\n```bash\npip install --user marko-backlinks\n```\n\nor install with `Poetry`\n\nThen you can see all the option of the CLI using\n\n```bash\nmarko-backlinks --help\n```\n\n</details>\n\n<details>\n  <summary>Installation as a pre-commit hook</summary>\nThis pre-commit hook use the [pre-commit](https://pre-commit.com) tool that you will\nneed to install.\n\nAdd the following line to your pre-commit configuration (`.pre-commit-config.yaml`) at the root of your \nrepository.\n\n```yaml\nrepos:\n-   repo: https://github.com/jb-delafosse/marko-backlinks\n    rev: v0.2.3\n    hooks:\n      - id: marko-backlinks\n        args: [\'directory-containing-my-markdown\']\n```\n\nand install the hook using `pre-commit install`\n</details>\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{marko-backlinks,\n  author = {jb-delafosse},\n  title = {Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/jb-delafosse/marko-backlinks}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'jb-delafosse',
    'author_email': 'jean-baptiste@lumapps.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jb-delafosse/marko-backlinks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

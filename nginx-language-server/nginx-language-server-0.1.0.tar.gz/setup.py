# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nginx_language_server', 'nginx_language_server.parser']

package_data = \
{'': ['*'], 'nginx_language_server': ['data/*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'crossplane>=0.5.7,<0.6.0', 'pygls>=0.9.1,<0.10.0']

entry_points = \
{'console_scripts': ['nginx-language-server = nginx_language_server.cli:cli']}

setup_kwargs = {
    'name': 'nginx-language-server',
    'version': '0.1.0',
    'description': 'A language server for nginx.conf',
    'long_description': '# Nginx Language Server\n\n[![image-version](https://img.shields.io/pypi/v/nginx-language-server.svg)](https://python.org/pypi/nginx-language-server)\n[![image-license](https://img.shields.io/pypi/l/nginx-language-server.svg)](https://python.org/pypi/nginx-language-server)\n[![image-python-versions](https://img.shields.io/pypi/pyversions/nginx-language-server.svg)](https://python.org/pypi/nginx-language-server)\n\nA [Language Server](https://microsoft.github.io/language-server-protocol/) for `nginx.conf`.\n\nStill under constructions, expect big changes and breaking changes for a while. Requires Python 3.8 for now, will probably relax in future.\n\n## Installation\n\nFrom your command line (bash / zsh), run:\n\n```bash\npip install -U nginx-language-server\n```\n\n`-U` ensures that you\'re pulling the latest version from pypi.\n\nAlternatively, consider using [pipx](https://github.com/pipxproject/pipx) to keep nginx-language-server isolated from your other Python dependencies.\n\n## Editor Setup\n\nThe following instructions show how to use nginx-language-server with your development tooling. The instructions assume you have already installed nginx-language-server.\n\n### Vim / Neovim\n\nWith [coc.nvim](https://github.com/neoclide/coc.nvim), put the following in `coc-settings.json`:\n\n```json\n  "languageserver": {\n    "nginx-language-server": {\n      "command": "nginx-language-server",\n      "filetypes": ["nginx"],\n      "rootPatterns": ["nginx.conf", ".git"]\n    }\n  },\n```\n\nNote: this list is non-exhaustive. If you know of a great choice not included in this list, please submit a PR!\n\n## Inspiration\n\nThe useful language data for nginx is ported from [vscode-nginx-conf-hint](https://github.com/hangxingliu/vscode-nginx-conf-hint). I would have used this library directly, but alas! It\'s written only for VSCode and I use Neovim.\n\n## Written by\n\nSamuel Roeca _samuel.roeca@gmail.com_\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pappasam/nginx-language-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

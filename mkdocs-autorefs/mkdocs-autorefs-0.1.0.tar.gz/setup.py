# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_autorefs']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11,<3.0',
 'Markdown>=3.3,<4.0',
 'MarkupSafe>=1.1,<2.0',
 'mkdocs>=1.1,<2.0',
 'pymdown-extensions>=6.3,<9.0',
 'pytkdocs>=0.2.0,<0.11.0']

entry_points = \
{'mkdocs.plugins': ['autorefs = mkdocs_autorefs.plugin:AutorefsPlugin']}

setup_kwargs = {
    'name': 'mkdocs-autorefs',
    'version': '0.1.0',
    'description': 'Automatically link across pages in MkDocs.',
    'long_description': '# mkdocs-autorefs\n\n[![ci](https://github.com/mkdocstrings/autorefs/workflows/ci/badge.svg)](https://github.com/mkdocstrings/autorefs/actions?query=workflow%3Aci)\n[![pypi version](https://img.shields.io/pypi/v/mkdocs-autorefs.svg)](https://pypi.org/project/mkdocs-autorefs/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocstrings/community)\n\nAutomatically link across pages in MkDocs.\n\n## Requirements\n\n`mkdocs-autorefs` requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install mkdocs-autorefs\n```\n',
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkdocstrings/autorefs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

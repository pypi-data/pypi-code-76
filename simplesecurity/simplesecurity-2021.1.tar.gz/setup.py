# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplesecurity']

package_data = \
{'': ['*']}

extras_require = \
{'full': ['poetry>=1.1.2,<3',
          'bandit>=1.6.2,<3',
          'safety>=1.9.0,<3',
          'dodgy>=0.2.1,<2',
          'dlint>=0.10.3,<2',
          'pygraudit>=27.1.1,<29',
          'semgrep>=0.27.0,<2']}

entry_points = \
{'console_scripts': ['simplesecurity = simplesecurity:cli']}

setup_kwargs = {
    'name': 'simplesecurity',
    'version': '2021.1',
    'description': 'Combine multiple popular python security tools and generate reports or output into different formats',
    'long_description': '[![Github top language](https://img.shields.io/github/languages/top/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)\n[![Codacy grade](https://img.shields.io/codacy/grade/.svg?style=for-the-badge)](https://www.codacy.com/gh/FHPythonUtils/SimpleSecurity)\n[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../)\n[![Issues](https://img.shields.io/github/issues/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../issues)\n[![License](https://img.shields.io/github/license/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](/LICENSE.md)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)\n[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/SimpleSecurity.svg?style=for-the-badge)](../../commits/master)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/SimpleSecurity.svg?style=for-the-badge)](https://pypi.org/project/SimpleSecurity/)\n[![PyPI Version](https://img.shields.io/pypi/v/SimpleSecurity.svg?style=for-the-badge)](https://pypi.org/project/SimpleSecurity/)\n\n<!-- omit in toc -->\n# SimpleSecurity\n\n<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">\n\n\nCombine multiple popular python security tools and generate reports or output\ninto different formats\n\nPlugins (these require the plugin executable in the system path. e.g. bandit\nrequires bandit to be in the system path...)\n\n- bandit\n- safety\n- dodgy\n- dlint\n- pygraudit\n- semgrep\n\nFormats\n\n- ansi (for terminal)\n- json\n- markdown\n- csv\n- sarif\n\n## Example Use\n\nSee below for the output if you run `simplesecurity` in this directory\n\n<img src="readme-assets/screenshots/sec.svg" width="500px">\n\n### Help\n\n```txt\nusage: __main__.py [-h] [--format FORMAT] [--plugin PLUGIN] [--file FILE] [--level LEVEL] [--confidence CONFIDENCE]\n                   [--no-colour] [--high-contrast] [--fast]\n\nCombine multiple popular python security tools and generate reports or output\ninto different formats\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --format FORMAT, -f FORMAT\n                        Output format. One of ansi, json, markdown, csv. default=ansi\n  --plugin PLUGIN, -p PLUGIN\n                        Plugin to use. One of bandit, safety, dodgy, dlint, pygraudit, semgrep, all, default=all\n  --file FILE, -o FILE  Filename to write to (omit for stdout)\n  --level LEVEL, -l LEVEL\n                        Minimum level/ severity to show\n  --confidence CONFIDENCE, -c CONFIDENCE\n                        Minimum confidence to show\n  --no-colour, -z       No ANSI colours\n  --high-contrast, -Z   High contrast colours\n  --fast, --skip        Skip long running jobs. Will omit plugins with long run time (applies to -p all only)\n```\n\nYou can also import this into your own project and use any of the functions\nin the DOCS\n\n<!-- omit in toc -->\n## Table of Contents\n- [Example Use](#example-use)\n\t- [Help](#help)\n- [Changelog](#changelog)\n- [Install With PIP](#install-with-pip)\n- [Developer Notes](#developer-notes)\n\t- [Generate semgrep_sec.yaml](#generate-semgrep_secyaml)\n- [Language information](#language-information)\n\t- [Built for](#built-for)\n- [Install Python on Windows](#install-python-on-windows)\n\t- [Chocolatey](#chocolatey)\n\t- [Download](#download)\n- [Install Python on Linux](#install-python-on-linux)\n\t- [Apt](#apt)\n- [How to run](#how-to-run)\n\t- [With VSCode](#with-vscode)\n\t- [From the Terminal](#from-the-terminal)\n- [Community Files](#community-files)\n\t- [Licence](#licence)\n\t- [Changelog](#changelog-1)\n\t- [Code of Conduct](#code-of-conduct)\n\t- [Contributing](#contributing)\n\t- [Security](#security)\n\t- [Support](#support)\n\n## Changelog\nSee the [CHANGELOG](/CHANGELOG.md) for more information.\n\n## Install With PIP\n\n**"Slim" Build:** Install bandit, dlint, dodgy, poetry, and safety with pipx\n\n```python\npip install simplesecurity\n```\n\n**Otherwise:**\n```python\npip install simplesecurity[full]\n```\n\nHead to https://pypi.org/project/SimpleSecurity/ for more info\n\n\n## Developer Notes\n\n### Generate semgrep_sec.yaml\n\n1. Clone https://github.com/returntocorp/semgrep-rules\n2. cd to project/python\n3. do\n   ```bash\n   $ cat **/security/**/*.yaml >> semgrep_sec.yaml\n   $ cat **/security/*.yaml >> semgrep_sec.yaml\n   ```\n4. Find and replace `rules:` with `` apart from the first instance\n5. Reformat with `ctrl+shift+i`\n6. replace simplesecurity/semgrep_sec.yaml with the new one\n\n## Language information\n### Built for\nThis program has been written for Python 3 and has been tested with\nPython version 3.9.0 <https://www.python.org/downloads/release/python-380/>.\n\n## Install Python on Windows\n### Chocolatey\n```powershell\nchoco install python\n```\n### Download\nTo install Python, go to <https://www.python.org/> and download the latest\nversion.\n\n## Install Python on Linux\n### Apt\n```bash\nsudo apt install python3.9\n```\n\n## How to run\n### With VSCode\n1. Open the .py file in vscode\n2. Ensure a python 3.9 interpreter is selected (Ctrl+Shift+P > Python:Select\nInterpreter > Python 3.9)\n3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)\n### From the Terminal\n```bash\n./[file].py\n```\n\n## Community Files\n### Licence\nMIT License\nCopyright (c) FredHappyface\n(See the [LICENSE](/LICENSE.md) for more information.)\n\n### Changelog\nSee the [Changelog](/CHANGELOG.md) for more information.\n\n### Code of Conduct\nIn the interest of fostering an open and welcoming environment, we\nas contributors and maintainers pledge to make participation in our\nproject and our community a harassment-free experience for everyone.\nPlease see the\n[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md) for more information.\n\n### Contributing\nContributions are welcome, please see the [Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md) for more information.\n\n### Security\nThank you for improving the security of the project, please see the [Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md) for more information.\n\n### Support\nThank you for using this project, I hope it is of use to you. Please be aware that\nthose involved with the project often do so for fun along with other commitments\n(such as work, family, etc). Please see the [Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md) for more information.\n',
    'author': 'FredHappyface',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FHPythonUtils/SimpleSecurity',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hycli', 'hycli.commands', 'hycli.commons', 'hycli.convert']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'XlsxWriter>=1.2.7,<2.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=7.0,<8.0',
 'filetype>=1.0.5,<2.0.0',
 'halo>=0.0.29,<0.0.32',
 'openpyxl>=3.0.5,<4.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.22.0,<3.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['hycli = hycli.cli:main']}

setup_kwargs = {
    'name': 'hycli',
    'version': '0.4.1',
    'description': 'Hypatos cli tool to batch extract documents through the API and to compare the results.',
    'long_description': '# Hycli\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hycli)](https://pypi.org/project/hycli/)\n[![PyPI version](https://badge.fury.io/py/hycli.svg)](https://pypi.org/project/hycli/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Main workflow](https://github.com/hypatos/hycli/workflows/Main%20workflow/badge.svg)\n\nThis repository contains a Python package/CLI tool to batch extract documents through the Hypatos API and to compare the results.\n\n## Quickstart\n\n```\npip install hycli\nhycli extract path-to-files [to-xlsx|to-csv|to-json] url\nhycli compare workbook1 workbook2\n```\n\nFor more information without leaving the cli use ```hycli --help```\n\n## API Reference and User Guide [available](https://hypatos.github.io/hycli/)\n\n---\n\n## Development\n\n### Requirement\n\n- [poetry](https://python-poetry.org/)\n\n### Installing\n\n```\npoetry install\npoetry shell\nhycli --help\n```\n\n### Running the tests\n\n```\npoetry run pytest\n```\n\n### Versioning\n\nUses [bump2version](https://github.com/c4urself/bump2version):\n\n```\nbump2version --verbose [patch|minor|major]  # add --dry-run to have a preview\ngit push --follow-tags\n```\n\n### Documentation\n\nIs build with sphinx, can be seen/worked on locally by:\n\n```\ncd docs\nmake html\nopen build/html/index.html\n```\n\n### License\n\nHypatos\n',
    'author': 'Dylan Bartels',
    'author_email': 'dylan.bartels@hypatos.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hypatos.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

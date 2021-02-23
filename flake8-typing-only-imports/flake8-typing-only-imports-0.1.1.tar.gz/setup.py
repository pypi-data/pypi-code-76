# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_typing_only_imports']

package_data = \
{'': ['*']}

entry_points = \
{'flake8.extension': ['TYO100 = flake8_typing_only_imports:Plugin']}

setup_kwargs = {
    'name': 'flake8-typing-only-imports',
    'version': '0.1.1',
    'description': 'A flake8 plugin that flags imports exclusively used for type annotations',
    'long_description': '<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/pypi/v/flake8-typing-only-imports.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/sondrelg/flake8-typing-only-imports">\n    <img src="https://codecov.io/gh/sondrelg/flake8-typing-only-imports/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://github.com/sondrelg/flake8-typing-only-imports/actions/workflows/testing.yml/badge.svg" alt="Test status">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# flake8-typing-only-imports\n\nflake8 plugin which flags imports which are exclusively used for type hinting.\n\n## Installation\n\n```shell\npip install flake8-typing-only-imports\n```\n\n## Codes\n\n| Code   | Description                                  |\n|--------|----------------------------------------------|\n| TYO100 | Import \'{module}\' only used for type hinting |\n\n## Rationale\n\nA common trade-off for annotating large code bases is you will end up with a\nlarge number of extra imports. In some cases, this can lead to\nimport circularity problems.\n\nOne (good) solution, as proposed in [PEP484](https://www.python.org/dev/peps/pep-0484/)\nis to use [forward references](https://www.python.org/dev/peps/pep-0484/#forward-references)\nand [type checking](https://www.python.org/dev/peps/pep-0484/#runtime-or-type-checking) blocks, like this:\n\n```python\nfrom typing import TYPE_CHECKING\n\n\nif TYPE_CHECKING:\n    from app.models import foo\n\n\ndef bar() -> \'foo\':\n    ...\n```\n\nAt the same time, this is often easier said than done, because in larger code bases you can be dealing\nwith hundreds of lines of imports for thousands of lines of code.\n\nThis plugin eliminates that problem by flagging imports which can be put inside a type-checking block.\n\n## As a pre-commit hook\n\nSee [pre-commit](https://github.com/pre-commit/pre-commit) for instructions\n\nSample `.pre-commit-config.yaml`:\n\n```yaml\n- repo: https://gitlab.com/pycqa/flake8\n  rev: 3.7.8\n  hooks:\n  - id: flake8\n    additional_dependencies: [flake8-typing-only-imports]\n```\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/flake8-typing-only-imports',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wu_diff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wu-diff',
    'version': '0.1.1',
    'description': 'Wu(O(NP)) algorithm',
    'long_description': '# wu-diff-python\n\nCompute difference between two lists using Wu\'s O(NP) algorithm.\n\n## Example\n\n```python\n>>> from wu_diff import WuDiff\n>>> print(WuDiff("strength", "string").str_diff())\n```\n```\n str\n-e\n+i\n ng\n-t\n-h\n```\n\n',
    'author': 'maiseaux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maiseaux/wu-diff-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

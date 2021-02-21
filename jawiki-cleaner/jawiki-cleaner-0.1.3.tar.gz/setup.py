# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jawiki_cleaner']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jawiki-cleaner = jawiki_cleaner.cli:main']}

setup_kwargs = {
    'name': 'jawiki-cleaner',
    'version': '0.1.3',
    'description': 'Japanese Wikipedia cleaner',
    'long_description': '# Japanese Wikipedia Cleaner\n\nApply extracted wikipedia text by WikiExtractor.\n\n\n```\n$ jawiki-cleaner --input ./wiki.txt --output ./cleaned-wiki.txt\n$ jawiki-cleaner -i ./wiki.txt -o ./cleaned-wiki.txt\n$ jawiki-cleaner -i ./wiki.txt # output path will be `./cleaned-wiki.txt`\n```',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpprc/jawiki-cleaner',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

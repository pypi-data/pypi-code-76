# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depending']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'depending',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Depending\n\nYet another dependency injection framework for python.\n\n## Usage\n\n```python\nimport asyncio\nfrom depending import dependency, bind, dependencies\n\n@dependency\nasync def name():\n    return "Item"\n\n@bind\nasync def function(name):\n    print(name)\n\nasync def main():\n    async with dependencies():\n        await function()\n\nasyncio.run(main())\n```\n\n',
    'author': 'Blake',
    'author_email': 'blakeinvictoria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

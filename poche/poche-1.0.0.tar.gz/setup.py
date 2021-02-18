# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poche']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poche',
    'version': '1.0.0',
    'description': 'Simple and fast Python in-memory caching library',
    'long_description': '# poche\n\n[![Build Status](https://travis-ci.org/etienne-napoleone/poche.svg?branch=main)](https://travis-ci.org/etienne-napoleone/poche)\n[![Codecov](https://codecov.io/gh/etienne-napoleone/poche/branch/main/graph/badge.svg)](https://codecov.io/gh/etienne-napoleone/poche)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSimple and fast Python in-memory caching with support for TTLs.\n\nMeant to speed up using dictionaries as cache backend for simple usecases.\n\nNo external dependencies, 100% code coverage and static type checked.\n\n## Installation\n\nRequires Python 3.6+.\n\n```bash\npip install poche\n```\n\n## Roadmap\n\nv1:\n\n- [x] Basic TTL\n- [x] `get`\n- [x] `set`\n- [x] `getset`\n- [x] `flush`\n\nv1.1:\n\n- [ ] `expire`\n- [ ] `persist`\n- [ ] `rename`\n\nv1.2:\n\n- [ ] `getorset` with callback\n\n## Example\n\n```python\nfrom time import sleep\n\nimport poche\n\n>>> c = poche.Cache()\n\n>>> c.set("one", "uno")\n>>> c.get("one")\n"uno"\n\n>>> c.get("two")\nNone\n>>> c.getset("two", "dos")\nNone\n>>> c.get("two")\n"dos"\n\n>>> c.set("three", "tres", ttl=2)\n>>> c.get("three")\n"tres"\n>>> sleep(2)\n>>> c.get("three")\nNone\n\n>>> c = poche.Cache(ttl=2)  # you can also define a default TTL\n\n>>> c.set("four", "cuatro")\n>>> c.get("four")\n"cuatro"\n>>> sleep(2)\n>>> c.get("four")\nNone\n```\n',
    'author': 'etienne-napoleone',
    'author_email': 'etienne.napoleone@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etienne-napoleone/poche',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

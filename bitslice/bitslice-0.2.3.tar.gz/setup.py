# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitslice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitslice',
    'version': '0.2.3',
    'description': 'Verilog-like bitvector slicing',
    'long_description': '# Bitslice\n\nVerilog-like bitslicing for Python.\n\n## Installation\n\nInstall the library from PyPI:\n~~~\npip install bitslice\n~~~\n\n## Quickstart\nBitslice is designed to behave as an integer value as much as possible.\nAll operators defined on `int` should be supported.\n\nBitslice adds the ability to extract or set one or more bits of the value:\n\n~~~ python\nfrom bitslice import Bitslice\nvalue = Bitslice(5, size=4)\nvalue[3:1] - 1\n~~~\n\nSee [bitslice.py](https://github.com/zegervdv/bitslice/blob/master/bitslice/bitslice.py) for more examples.\n',
    'author': 'Zeger Van de Vannet',
    'author_email': 'zegervdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zegervdv/bitslice',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['dask[array]', 'fsspec', 'gcsfs', 'pandas', 'xarray', 'zarr']

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '0.4.0a0',
    'description': 'A package for accessing MalariaGEN public data.',
    'long_description': None,
    'author': 'Alistair Miles',
    'author_email': 'alimanfoo@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)

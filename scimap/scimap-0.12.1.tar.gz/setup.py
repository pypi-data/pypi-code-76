# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scimap',
 'scimap.archive',
 'scimap.helpers',
 'scimap.plotting',
 'scimap.preprocessing',
 'scimap.tests',
 'scimap.tools']

package_data = \
{'': ['*'], 'scimap.tests': ['_data/*']}

install_requires = \
['PhenoGraph>=1.5.7,<2.0.0',
 'TiffFile>=2020.11.18,<2021.0.0',
 'anndata>=0.7.4,<0.8.0',
 'dask[array]>=2.30.0,<3.0.0',
 'llvmlite<=0.34.0',
 'matplotlib>=3.2.1,<4.0.0',
 'mkdocs>=1.1.2,<2.0.0',
 'napari>=0.4.2,<0.5.0',
 'numba<=0.51.2',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'plotly>=4.12.0,<5.0.0',
 'pytest-xvfb>=2.0.0,<3.0.0',
 'pytest>=5.4.3,<6.0.0',
 'scanpy>=1.6.0,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'shapely>=1.7.1,<2.0.0',
 'sklearn>=0.0,<0.1',
 'tifffile>=2020.6.3,<2021.0.0',
 'zarr>=2.5.0,<3.0.0']

entry_points = \
{'console_scripts': ['scimap = scimap.cli:main']}

setup_kwargs = {
    'name': 'scimap',
    'version': '0.12.1',
    'description': 'Single-Cell Image Analysis Package',
    'long_description': '# Single-Cell Image Analysis Package\n\nScimap is a scalable toolkit for analyzing single-cell multiplex imaging data. The package uses the [anndata](https://anndata.readthedocs.io/en/stable/anndata.AnnData.html) framework making it easy to integrate with other popular single-cell analysis toolkits such as [scanpy](https://scanpy.readthedocs.io/en/latest/#). It includes preprocessing, phenotyping, visualization, clustering, spatial analysis and differential spatial testing. The Python-based implementation efficiently deals with datasets of more than one million cells.\n\n\n[![Unix Build Status](https://img.shields.io/travis/ajitjohnson/scimap/master.svg?label=unix)](https://travis-ci.org/ajitjohnson/scimap)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/ajitjohnson/scimap/master.svg?label=windows)](https://ci.appveyor.com/project/ajitjohnson/scimap)\n[![Documentation Status](https://readthedocs.org/projects/scimap-doc/badge/?version=latest)](https://scimap-doc.readthedocs.io/en/latest/?badge=latest)\n[![Downloads](https://pepy.tech/badge/scimap)](https://pepy.tech/project/scimap)\n[![PyPI Version](https://img.shields.io/pypi/v/scimap.svg)](https://pypi.org/project/scimap)\n[![PyPI License](https://img.shields.io/pypi/l/scimap.svg)](https://pypi.org/project/scimap)\n<!--[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/ajitjohnson/scimap.svg)](https://scrutinizer-ci.com/g/ajitjohnson/scimap/?branch=master)-->\n<!--[![Coverage Status](https://img.shields.io/coveralls/ajitjohnson/scimap/master.svg)](https://coveralls.io/r/ajitjohnson/scimap) -->\n\n## Installation\n\nWe strongly recommend installing `scimap` in a fresh virtual environment.\n\n```\n# If you have conda installed\nconda create --name scimap python=3.7\nconda activate scimap\n```\n\nInstall `scimap` directly into an activated virtual environment:\n\n```python\n$ pip install scimap\n$ pip install napari[all] # For visualizing images\n```\n\nAfter installation, the package can be imported as:\n\n```python\n$ python\n>>> import scimap as sm\n```\n\n## Get Started\n\n\n#### Detailed documentation of `scimap` functions and tutorials are available [here](https://scimap-doc.readthedocs.io/en/latest/).\n',
    'author': 'Ajit Johnson Nirmal',
    'author_email': 'ajitjohnson.n@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/scimap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

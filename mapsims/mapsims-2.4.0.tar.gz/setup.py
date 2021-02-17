# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapsims', 'mapsims.data', 'mapsims.extern', 'mapsims.tests']

package_data = \
{'': ['*'],
 'mapsims.data': ['planck_deltabandpass/*',
                  'simonsobs_instrument_parameters_2020.06/*'],
 'mapsims.tests': ['data/*']}

install_requires = \
['astropy>=4,<5',
 'healpy>=1.14.0,<2.0.0',
 'numpy>=1.18.0,<2.0.0',
 'pixell>=0.10.3,<0.11.0',
 'pysm3>=3.3.0,<4.0.0',
 'pyyaml>=5,<6',
 'so-pysm-models>=2.4.0,<3.0.0',
 'so_noise_models==3.1.1',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.4.0,<4.0.0'],
 'test': ['pytest>=5.4.3,<6.0.0',
          'pytest-astropy>=0.8.0,<0.9.0',
          'mpi4py>=3.0.3,<4.0.0',
          'nbval>=0.9.6,<0.10.0',
          'jupyter_client>=6.1.7,<7.0.0',
          'ipykernel>=5.3.4,<6.0.0',
          'nbformat>=5.0.7,<6.0.0']}

entry_points = \
{'console_scripts': ['mapsims_run = mapsims.runner:command_line_script']}

setup_kwargs = {
    'name': 'mapsims',
    'version': '2.4.0',
    'description': 'Map based simulations package for Cosmic Microwave Background experiments',
    'long_description': 'Map based simulations package\n-----------------------------\n\n![Build status](https://github.com/simonsobs/mapsims/workflows/Python%20package/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/mapsims/badge/?version=latest)](https://mapsims.readthedocs.io/en/latest/?badge=latest)\n\nMap based simulations package for Simons Observatory,\nmaintained by the Map-Based Simulation Pipeline Working Group (MBS)\n\n* For documentation, see <https://mapsims.readthedocs.io/>\n* For simulation results see <https://github.com/simonsobs/map_based_simulations>\n* [Wiki page, restricted access](http://simonsobservatory.wikidot.com/pwg:mbs)\n',
    'author': 'Andrea Zonca',
    'author_email': 'code@andreazonca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonsobs/mapsims',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

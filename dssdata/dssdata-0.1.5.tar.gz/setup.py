# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dssdata',
 'dssdata.decorators',
 'dssdata.pfmodes',
 'dssdata.reductions',
 'dssdata.reductions.regs',
 'dssdata.tools',
 'dssdata.tools.lines',
 'dssdata.tools.losses',
 'dssdata.tools.regs',
 'dssdata.tools.voltages']

package_data = \
{'': ['*']}

install_requires = \
['OpenDSSDirect.py', 'pandas']

setup_kwargs = {
    'name': 'dssdata',
    'version': '0.1.5',
    'description': 'Organizing OpenDSS data',
    'long_description': "# DSSData\n\n\n_**⚡A python micro-framework for steady-state simulation and data analysis of electrical distribution systems modeled on [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).**_\n\nMode support: Static and Time-series.\n\n## Why DSSData?\n\nThe propose of DSSData is to facilitate the steady-state simulation of modern electrical distribution systems, such as microgrid, smart grids, and smart cities.\n\nWith DSSData you can easily make your own super new fancy operation strategies with storage or generators, probabilistic simulation, or a simple impact studies of a distributed generator. See an example in our [Tutorial](https://felipemarkson.github.io/dssdata/tutorial/).\n\n**_All you need is your base distribution system modeled in OpenDSS!!!_**\n\n### Easy to simulate\n\nWe built the DSSData for you just write what you want in a simple function, plugin on a power flow mode, and run. \n\nYou don't need anymore write a routine to run each power flow per time. \n\n## Documentation\n\nSee [DSSData Documentation](https://felipemarkson.github.io/dssdata).\n\n## Installation\n\nWe strongly recommend the use of virtual environments manager.\n\n### Using pip\n\n```console\npip install dssdata\n```\n\n### Using poetry\n\n```console\npoetry add dssdata\n```\n\n## Help us to improve DSSData\n\nSee our [Issue](https://github.com/felipemarkson/dssdata/issues) section!\n\n\n## Contributors: \n\n- [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)\n",
    'author': 'Felipe M. S. Monteiro',
    'author_email': 'fmarkson@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipemarkson/dssdata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

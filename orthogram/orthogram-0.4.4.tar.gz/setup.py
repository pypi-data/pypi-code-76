# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orthogram']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'networkx>=2.5,<3.0',
 'svgwrite>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'orthogram',
    'version': '0.4.4',
    'description': 'Draw block diagrams.',
    'long_description': 'Orthogram\n=========\n\nOrthogram is a command line program and Python library that lets you\ndraw block diagrams.  It reads the definition of a diagram from a YAML\nfile and produces a SVG file like this one:\n\n.. image:: examples/showoff.svg\n   :width: 100%\n   :alt: (Showing off the capabilities)\n\nTarget audience\n---------------\n\nThis project might be of interest to you if:\n\n* You do not want to use a GUI.  You prefer your diagrams defined in\n  plain text files.\n* You know where your blocks should be, but you would rather have the\n  computer maintain the connections for you.\n* You tried to force `Graphviz`_ or `PlantUML`_ to output the layout\n  you want, but to no avail.\n\n.. _Graphviz: https://graphviz.org/\n.. _PlantUML: https://plantuml.com/\n\nInstallation and usage\n----------------------\n\nInstall from PyPI:\n\n.. code::\n   \n   pip install orthogram\n\nAssuming there is a diagram definition file named ``diagram.yaml`` in\nyour current directory, run the following command to produce a SVG\nfile:\n\n.. code::\n   \n   python -m orthogram diagram.yaml\n\nPlease read the full online `documentation`_ for more.\n\n.. _documentation: https://orthogram.readthedocs.org\n',
    'author': 'Georgios Athanasiou',
    'author_email': 'yorgath@gmail.com',
    'maintainer': 'Georgios Athanasiou',
    'maintainer_email': 'yorgath@gmail.com',
    'url': 'https://github.com/yorgath/orthogram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

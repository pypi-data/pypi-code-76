# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxcontrib', 'sphinxcontrib.nvd3']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.5.0,<4.0.0', 'python-nvd3>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'sphinxcontrib.nvd3',
    'version': '0.2.1',
    'description': 'Sphinx chart extension using NVD3.js.',
    'long_description': '====================\n sphinxcontrib.nvd3\n====================\n\n.. image:: https://github.com/shkumagai/sphinxcontrib.nvd3/workflows/Test/badge.svg?branch=master\n    :target: https://github.com/shkumagai/sphinxcontrib.nvd3/workflows/Test/badge.svg?branch=master\n    :alt: master\n\n.. image:: https://readthedocs.org/projects/sphinxcontribnvd3/badge/?version=latest\n    :target: https://sphinxcontribnvd3.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/v/sphinxcontrib.nvd3.svg\n    :target: https://pypi.org/project/sphinxcontrib.nvd3/\n    :alt: Latest\n\n.. image:: https://img.shields.io/pypi/pyversions/sphinxcontrib.nvd3.svg\n    :target: https://pypi.org/project/sphinxcontrib.nvd3/\n    :alt: Python Versions\n\n.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg\n    :target: https://github.com/shkumagai/sphinxcontrib.nvd3/blob/master/LICENSE\n    :alt: License\n\nSphinx chart extension using NVD3.\n\n\nFeature\n=======\n* provide some kinds of ``nvd3-`` prefixed directives to generate SVG chart from source.\n\n\nInstallation\n============\nInstall with pip::\n\n    $ pip install sphinxcontrib.nvd3\n\n\nsetup conf.py with::\n\n    extensions = ["sphinxcontrib.nvd3"]\n\nThis package is NOT includes Javascript and CSS files (e.g. d3.js, nvd3.js and nvd3.css).\n\nYou need to add `setup` function into conf.py, as below::\n\n    def setup(app):\n        app.add_js_file("/path/to/d3.v3.js")\n        app.add_js_file("/path/to/nv.d3.js")\n        app.add_css_file("/path/to/nv.d3.css")\n\nAnd then::\n\n    $ make html\n\n\nRequirement\n===========\n* python-nvd3 >= 0.13.10\n* D3.js >= 3.0,<4.0\n* Sphinx >= 3.0\n\n\nLicense\n=======\n\nLicensed under the `Apache Software License <http://opensource.org/licenses/Apache-2.0>`_ .\nSee the LICENSE file for specific terms.\n\n\n.. END\n',
    'author': 'shkumagai',
    'author_email': 'take.this.2.your.grave@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shkumagai/sphinxcontrib.nvd3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

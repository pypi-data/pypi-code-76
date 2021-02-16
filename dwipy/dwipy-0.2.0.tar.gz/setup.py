# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dwipy', 'dwipy.IO', 'dwipy.metrics', 'dwipy.mrtrix']

package_data = \
{'': ['*']}

install_requires = \
['SimpleITK>=2.0.2,<3.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pydicom>=2.1.1,<3.0.0',
 'pytesseract>=0.3.6,<0.4.0']

setup_kwargs = {
    'name': 'dwipy',
    'version': '0.2.0',
    'description': 'DWI anaylysis pipeline',
    'long_description': '# dwipy\n\n[![Build Status](https://github.com/svdvoort/dwipy/workflows/test/badge.svg?branch=master&event=push)](https://github.com/svdvoort/dwipy/actions?query=workflow%3Atest)\n[![Python Version](https://img.shields.io/pypi/pyversions/dwipy.svg)](https://pypi.org/project/dwipy/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nDWI analysis pipeline\n\nMade for  the initial analysis of diffusion data, especially for extracting the b-values and b-vectors from DICOM data, to allow for further processing.\n\n## Installation\n\nThis package requires the installation of Tesseract 4.1.1: https://medium.com/quantrium-tech/installing-tesseract-4-on-ubuntu-18-04-b6fcd0cbd78f\nAnd mtrix: https://mrtrix.readthedocs.io/en/latest/\n\n```bash\npip install dwipy\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/svdvoort/dwipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.9',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentipy', 'sentipy.lib']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.4,<2.0.0']

setup_kwargs = {
    'name': 'sentipy',
    'version': '0.2.0',
    'description': 'Python implementations of Sentinel 2 Toolbox L2 products & spectral indices',
    'long_description': '\nPython implementations of Sentinel 2 Toolbox L2 products & spectral indices\n\n.. image:: https://github.com/UpstatePedro/sentipy/workflows/Run%20tests/badge.svg\n\nsentipy is a small package that aims to do one thing well: provide an easy-to-use python API for processing sentinel\nsatellite raster data into useful biophysical estimates and spectral indices.\n\nInstallation\n-------------\n\nThe sentipy package is built & published (with enormous gratitude) using `Poetry <https://python-poetry.org/>`_\n\n.. code-block:: bash\n\n    $ pip install sentipy\n\nDocumentation\n-------------\n\n.. image:: https://readthedocs.org/projects/sentipy/badge/?version=latest\n   :target: https://sentipy.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\nDocumentation for the project is hosted at `Read the Docs <https://sentipy.rtfd.io>`_\n\nProject status\n--------------\n\nThis is a hobby project in the early stages of development, please do not rely on feature or API stability!',
    'author': 'UpstatePedro',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UpstatePedro/sentipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

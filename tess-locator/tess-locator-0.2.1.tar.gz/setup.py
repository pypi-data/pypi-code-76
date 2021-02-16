# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_locator']

package_data = \
{'': ['*'], 'tess_locator': ['data/*']}

install_requires = \
['astropy-healpix>=0.5',
 'astropy>=4.0',
 'attrs>=20.3.0',
 'backoff>=1.10.0',
 'httpx>=0.16.1',
 'numpy>=1.19',
 'pandas>=1.0',
 'pyarrow>=1.0.1',
 'tqdm>=4.51',
 'typer>=0.3.2']

setup_kwargs = {
    'name': 'tess-locator',
    'version': '0.2.1',
    'description': 'Fast offline queries of TESS FFI positions and filenames.',
    'long_description': 'tess-locator\n============\n\n**Fast offline queries of TESS FFI positions and url\'s.**\n\n|pypi| |pytest| |black| |flake8| |mypy|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-locator\n                :target: https://pypi.python.org/pypi/tess-locator\n.. |pytest| image:: https://github.com/SSDataLab/tess-locator/workflows/pytest/badge.svg\n.. |black| image:: https://github.com/SSDataLab/tess-locator/workflows/black/badge.svg\n.. |flake8| image:: https://github.com/SSDataLab/tess-locator/workflows/flake8/badge.svg\n.. |mypy| image:: https://github.com/SSDataLab/tess-locator/workflows/mypy/badge.svg\n\n\n`tess-locator` is a user-friendly package which provides fast offline access to an embedded database of TESS Full-Frame Image (FFI) meta data.\nIt allows TESS pixel coordinates and FFI filenames to be queried in a fast way without requiring internet access.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-locator\n\nExample use\n-----------\n\nConverting celestial to pixel coordinates:\n\n.. code-block:: python\n\n    >>> from tess_locator import locate\n    >>> locate("Alpha Cen")\n    List of 2 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1700.2, row=1860.3, time=None)\n      TessCoord(sector=12, camera=2, ccd=1, column=360.7, row=1838.8, time=None)]\n\n\nObtaining pixel coordinates for a specific time:\n\n.. code-block:: python\n\n    >>> locate("Alpha Cen", time="2019-04-28")\n    List of 1 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1700.2, row=1860.3, time=2019-04-28 00:00:00)]\n\n\nObtaining FFI image meta data:\n\n.. code-block:: python\n\n    >>> locate("Alpha Cen")[0].get_images()\n    List of 1248 images\n    ↳[TessImage(filename=\'tess2019113062933-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-04-23 06:34:41\', end=\'2019-04-23 07:04:41\')\n      TessImage(filename=\'tess2019113065933-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-04-23 07:04:41\', end=\'2019-04-23 07:34:41\')\n      TessImage(filename=\'tess2019113072933-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-04-23 07:34:41\', end=\'2019-04-23 08:04:41\')\n      TessImage(filename=\'tess2019113075933-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-04-23 08:04:41\', end=\'2019-04-23 08:34:41\')\n      ...\n      TessImage(filename=\'tess2019140065932-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-05-20 07:05:08\', end=\'2019-05-20 07:35:08\')\n      TessImage(filename=\'tess2019140072932-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-05-20 07:35:08\', end=\'2019-05-20 08:05:08\')\n      TessImage(filename=\'tess2019140075932-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-05-20 08:05:08\', end=\'2019-05-20 08:35:08\')\n      TessImage(filename=\'tess2019140082932-s0011-2-2-0143-s_ffic.fits\', begin=\'2019-05-20 08:35:08\', end=\'2019-05-20 09:05:08\')]\n\n\nDocumentation\n-------------\n\nPlease visit the `tutorial <https://github.com/SSDataLab/tess-locator/blob/master/docs/tutorial.ipynb>`_.\n\n\nSimilar packages\n----------------\n\n* `tess-point <https://github.com/christopherburke/tess-point>`_ uses a theoretical pointing model rather than the WCS data. It should agree with the WCS results to within 1-2 pixels. Compared to `tess-point`, we add a user-friendly API and the ability to specify the time, which is important for moving objects.\n* `astroquery.mast <https://astroquery.readthedocs.io/en/latest/mast/mast.html>`_ includes the excellent ``TesscutClass.get_sectors()`` method which queries a web API. This package provides an offline version of that service, and adds the ability to query by time.\n* `tess-waldo <https://github.com/SimonJMurphy/tess-waldo>`_ lets you visualize how a target moves over the detector across sectors. It queries the ``TessCut`` service to obtain this information. This package adds the ability to create such plots offline.\n',
    'author': 'Geert Barentsen',
    'author_email': 'hello@geert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SSDataLab/tess-locator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

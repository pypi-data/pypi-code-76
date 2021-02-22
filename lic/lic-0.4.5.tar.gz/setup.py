# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lic']

package_data = \
{'': ['*'],
 'lic': ['.mypy_cache/*',
         '.mypy_cache/3.7/*',
         '.mypy_cache/3.7/_typeshed/*',
         '.mypy_cache/3.7/collections/*',
         '.mypy_cache/3.7/ctypes/*',
         '.mypy_cache/3.7/importlib/*',
         '.mypy_cache/3.7/lic/*',
         '.mypy_cache/3.7/logging/*',
         '.mypy_cache/3.7/multiprocessing/*',
         '.mypy_cache/3.7/os/*']}

install_requires = \
['imageio>=2.8.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'tqdm>=4.47.0,<5.0.0']

entry_points = \
{'console_scripts': ['lic = lic.lic_main:run']}

setup_kwargs = {
    'name': 'lic',
    'version': '0.4.5',
    'description': 'Line integral convolution for numpy arrays',
    'long_description': '.. image:: https://img.shields.io/pypi/v/lic?style=flat-square\n   :target: https://pypi.org/project/lic/\n   :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/l/lic?style=flat-square\n   :target: https://gitlab.com/szs/lic/-/raw/master/LICENSE\n   :alt: PyPI - License\n\n.. image:: https://img.shields.io/pypi/pyversions/lic?style=flat-square\n   :target: https://python.org\n   :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/gitlab/pipeline/szs/lic?style=flat-square\n   :target: https://gitlab.com/szs/lic/-/pipelines\n   :alt: Gitlab pipeline status\n\n.. image:: https://gitlab.com/szs/lic/badges/master/coverage.svg?style=flat-square\n   :target: https://gitlab.com/szs/lic/-/pipelines\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/lic/badge/?version=latest\n   :target: https://lic.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n⎣⫯ℂ: Line Integral Convolution for numpy Arrays\n===============================================\n\nThis package provides line integral convolution (lic) algorithms to Python.\n\n.. figure:: https://gitlab.com/szs/lic/-/raw/master/docs/build/html/_images/KH3.png\n   :alt: lic image of the Kelvin-Helmholtz instability\n\n   lic image of the Kelvin-Helmholtz instability\n\nThere are functions which can be imported and are highly configurable for the power user.\nMoreover, there is a command line tool to generate lic images without having to code a single line.\n\nInstallation\n============\n\nThe installation is straight forward. You can install the package via ``pip``, ``pipenv``, ``poetry``\nand alike or by downloading the source from the gitlab repository.\n\nFrom pypi.org (recommended)\n---------------------------\n\nInstall by typing\n\n.. code-block:: shell\n\n                pip install lic\n\nor\n\n.. code-block:: shell\n\n                pip install --user lic\n\nif you do not have root access.\n\nPlease check the documentations for `pipenv <https://pipenv.pypa.io/en/latest/>`_, and\n`poetry <https://python-poetry.org/docs/>`_ for information on how to install packages with these tools.\n\nFrom gitlab.com\n---------------\n\nTo get the latest features or contribute to the development, you can clone the whole project using\n`git <https://git-scm.com/>`_:\n\n.. code-block:: shell\n\n                git clone https://gitlab.com/szs/lic.git\n\nNow you can, for instance, copy ``lic.py`` over to your project and import it directly or use it as a\ncommand line tool.\n\nUsage\n=====\n\nYou can import lic in your program and use the functions directly or use the command line tool.\n\nImporting the module\n--------------------\n\nOnce the package is installed where Python can find it, you can use the function ``lic`` directly.\n\n.. code-block:: Python3\n\n                import lic\n                import matplotlib.pyplot as plt\n\n                # ... get x and y arrays from somewhere ...\n\n                lic_result = lic.lic(x, y, length=30)\n\n                plt.imshow(lic_result, origin=\'lower\', cmap=\'gray\')\n                plt.show()\n\nFind out more about the options by reading the source documentation:\n\n.. code-block:: shell\n\n                pydoc lic.lic\n\nYou can also control the seed, i.e., the underlying texture for the lic:\n\n.. code-block:: shell\n\n                pydoc lic.gen_seed\n\nYou can run the example from the root folder to see the result:\n\n.. code-block:: shell\n\n                PYTHONPATH="." python3 examples/ex1.py\n\nCommand Line Tool\n-----------------\n\nYou will need npy data files (saved using numpy.save) to use lic from the command line:\n\n.. code-block:: shell\n\n                lic data_x.npy data_y.npy -v -l 30 -c\n\nSee ``lic --help`` for a full list of options.\n\nHow to Contribute\n=================\n\nIf you find a bug, want to propose a feature or need help getting this package to work with your data\non your system, please don\'t hesitate to file an `issue <https://gitlab.com/szs/lic/-/issues>`_ or write\nan email. Merge requests are also much appreciated!\n\nProject links\n=============\n\n* `Repository <https://gitlab.com/szs/lic>`_\n* `Documentation <https://lic.readthedocs.io/en/latest/>`_\n* `pypi page <https://pypi.org/project/lic/>`_\n\nExternal links\n==============\n\n* http://www.zhanpingliu.org/Research/FlowVis/LIC/LIC.htm\n* https://www3.nd.edu/~cwang11/2dflowvis.html\n',
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/szs/lic/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

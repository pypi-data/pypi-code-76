# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kallisto', 'kallisto.data', 'kallisto.reader', 'kallisto.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'flake8>=3.8.4,<4.0.0',
 'numpy>=1.19.0,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

entry_points = \
{'console_scripts': ['kallisto = kallisto.console:cli']}

setup_kwargs = {
    'name': 'kallisto',
    'version': '1.0.3',
    'description': 'The Kallisto software enables the efficient calculation of atomic features that can be used within a quantitative structure-activity relationship (QSAR) approach. Furthermore, several modelling helpers are implemented.',
    'long_description': '<div align="center">\n<img src="./assets/logo.svg" alt="Kallisto" width="300">\n</div>\n\n##\n\n[![Documentation](https://img.shields.io/badge/GitBook-Docu-lightgrey)](https://app.gitbook.com/@ehjc/s/kallisto/)\n[![License](https://img.shields.io/badge/license-Apache%202-blue)](https://img.shields.io/badge/license-Apache%202-blue)\n[![Maturity Level](https://img.shields.io/badge/Maturity%20Level-ML--1-orange)](https://img.shields.io/badge/Maturity%20Level-ML--1-orange)\n[![Tests](https://github.com/AstraZeneca/kallisto/workflows/Tests/badge.svg)](https://github.com/AstraZeneca/kallisto/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/AstraZeneca/kallisto/branch/master/graph/badge.svg?token=HI0U0R96X8)](https://codecov.io/gh/AstraZeneca/kallisto)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n\nTable of Contents\n-----------------\n\n- Full Author List\n- Introduction\n- Installation\n- Reference\n\nFull Author List\n----------------\n\nEike Caldeweyher and Philipp Pracht\n\nIntroduction\n------------\n\nWe developed the `kallisto` program for the efficient and robust calculation of atomic features using molecular geometries either in a ``xmol`` or a ``Turbomole`` format.\nFurthermore, several modelling tools are implemented, e.g., to calculate root-mean squared deviations via quaternions (including rotation matrices), sorting of molecular geometries and many more. All features of ``kallisto`` are described in detail within our [documentation](https://app.gitbook.com/@ehjc/s/kallisto/) ([GitBook repository](https://github.com/f3rmion/gitbook-kallisto)).\n\nInstallation from PyPI\n----------------------\n\nTo install ``kallisto`` via `pip` use our published PyPI package\n```bash\npip install kallisto\n```\n\nInstallation from Source\n------------------------\n\n`kallisto` runs on `python3`\n\nPython development setup. Install the `pyenv` python version manager:\n```bash\ncurl https://pyenv.run | bash\n```\nand add this to the `~/.bashrc` and source it:\n```bash\nexport PATH="~/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n```\nInstall the latest python versions:\n```bash\npyenv install 3.8.2\npyenv install 3.7.7\npyenv local 3.8.2 3.7.7\n```\n\nNow we are ready to set up `kallisto`.\nClone the repository:\n```bash\ngit clone git@github.com:AstraZeneca/kallisto.git\n```\n\nInstall a python dependency manager. We choose to go with `poetry`:\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\nsource ~/.poetry/env\n```\nor alternatively via `pip`:\n```bash\npip install --user poetry\n```\n\nNow, if you haven\'t already done so, change into the cloned `kallisto` directory and\ndownload the dependencies via `poetry`:\n```bash\ncd kallisto\npoetry install\n```\n\nFinally install the test automation environment `nox` via ``pip``:\n```bash\npip install --user --upgrade nox\n```\n\nRun `nox` to test the setup.\n\nReference\n---------\n\ntba\n',
    'author': 'Eike Caldeweyher',
    'author_email': 'hello@eikecaldeweyher.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/kallisto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

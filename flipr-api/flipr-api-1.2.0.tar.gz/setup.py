# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flipr_api']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.7.0,<3.0.0', 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['flipr-api = flipr_api.__main__:main']}

setup_kwargs = {
    'name': 'flipr-api',
    'version': '1.2.0',
    'description': 'Python client for flipr API.',
    'long_description': "Flipr Python API REST Client\n============================\nClient Python pour l'API Flipr. | Python client for Flipr API.\n\n|PyPI| |GitHub Release| |Python Version| |License| |Black|\n\n|Read the Docs| |Codecov| |GitHub Activity|\n\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/flipr-api\n   :target: https://pypi.org/project/flipr-api/\n   :alt: PyPI\n.. |GitHub Release| image:: https://img.shields.io/github/release/cnico/flipr-api.svg\n   :target: https://github.com/cnico/flipr-api/releases\n   :alt: GitHub Release\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/flipr-api\n   :target: https://pypi.org/project/flipr-api/\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/flipr-api\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/flipr-api/latest.svg?label=Read%20the%20Docs\n   :target: https://flipr-api.readthedocs.io/\n   :alt: Read the documentation at https://flipr-api.readthedocs.io/\n.. |Codecov| image:: https://codecov.io/gh/cnico/flipr-api/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/cnico/flipr-api\n   :alt: Codecov\n.. |GitHub Activity| image:: https://img.shields.io/github/commit-activity/y/cnico/flipr-api.svg\n   :target: https://github.com/cnico/flipr-api/commits/master\n   :alt: GitHub Activity\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nYou will find English README content in the section `For English speaking users`_.\n\nVous trouverez le contenu francophone du README dans la section `Pour les francophones`_.\n\nPour les francophones\n---------------------\n\nDescription\n^^^^^^^^^^^\n\nFlipr est un objet connecté que l'on met dans sa piscine pour mesurer en continu les valeurs chimiques de celle-ci.\nCe package Python permet de gérer la communication avec l'API REST publique `Flipr <https://apis.goflipr.com/Help>`_.\n\nLe client permet de :\n* Récupérer l'id de votre flipr.\n* Accéder à la mesure la plus récente de votre Flipr (données de température, ph, chlore et redox).\n\nPour utiliser le client, il vous faudra disposer de vos identifiants et mot de passe Flipr créés avec l'application mobile.\n\nCe package a été développé avec l'intention d'être utilisé par `Home-Assistant <https://home-assistant.io/>`_\nmais il peut être utilisé dans d'autres contextes.\n\nInstallation\n^^^^^^^^^^^^\n\nPour utiliser le module Python ``flipr_api`` vous devez en premier installer\nle package en utilisant pip_ depuis PyPI_:\n\n.. code:: console\n\n   $ pip install flipr-api\n\n\nVous pouvez trouver un exemple d'usage en regardant\n`le test d'intégration <tests/test_integrations.py>`_.\n\nContribuer\n^^^^^^^^^^\n\nLes contributions sont les bienvenues. Veuillez consulter les bonnes pratiques\ndétaillées dans `CONTRIBUTING.rst`_.\n\n\nFor English speaking users\n--------------------------\n\nDescription En\n^^^^^^^^^^^^^^\n\nFlipr is a connect object that you put in your swimming pool in order to measure chemical values of it.\nThis Python package allows to communicate with the public REST API `Flipr <https://apis.goflipr.com/Help>`_.\n\nThis client allows to :\n* Retrieve the id of your flipr\n* Get the latest measure of your Flipr (data of temperature, ph, chlorine and redox).\n\nTo use this client, it requires you have your login and password created with Flipr's mobile application.\n\nThis package has been developed to be used with `Home-Assistant <https://home-assistant.io/>`_\nbut it can be used in other contexts.\n\nInstallation\n^^^^^^^^^^^^\n\nTo use the ``flipr_api`` Python module, you have to install this package first via\npip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install flipr-api\n\nYou will find an example ot usage in a Python program in the `integration test <tests/test_integrations.py>`_.\n\nContributing\n^^^^^^^^^^^^\n\nContributions are welcomed. Please check the guidelines in `CONTRIBUTING.rst`_.\n\n\nCredits\n-------\n\nThis project was inspired from the MeteoFranceAPI_ HACF project.\n\n.. _MeteoFranceAPI: https://github.com/hacf-fr/meteofrance-api\n.. _PyPI: https://pypi.org/\n.. _pip: https://pip.pypa.io/\n.. _CONTRIBUTING.rst: CONTRIBUTING.rst\n",
    'author': 'cnico',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cnico/flipr-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

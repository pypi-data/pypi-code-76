# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trailhead_scraper']
install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'trailhead-scraper',
    'version': '0.1.1',
    'description': 'Retrieve public data from Salesforce Trailhead user profiles',
    'long_description': '===================\nTrailhead Scraper\n===================\n\n|license|   |tests|\n\n.. |license| image:: https://shields.io/badge/License-MIT-blue\n\n.. |tests| image:: https://github.com/ang3orge/trailhead-scraper/workflows/Tests/badge.svg\n   :alt: Trailhead Scraper Tests status on GitHub Actions\n   :target: https://github.com/ang3orge/trailhead-scraper/actions\n\nA simple package that enables retrieval of public data from Salesforce Trailhead user profiles.\n\nInstallation\n------------\n\ntrailhead-scraper can be installed via ``pip``:\n\n.. code-block:: sh\n\n   $ pip install trailhead-scraper\n\nQuickstart\n----------\n\nYou can now retrieve information about a Trailhead user based on a username:\n\n.. code-block:: python\n\n   from trailhead_scraper import fetch_profile_data, fetch_rank_data, fetch_awards\n\n   username = "trailhead-username"\n\n   # get profile information\n   profile = fetch_profile_data(username)\n\n   # get rank information\n   rank_data = fetch_rank_data(username)\n\n   # get list of awards (badges)\n   awards = fetch_awards(username)\n\nUse the profile data to access basic information about the user:\n\n.. code-block:: python\n\n   print(profile["profilePhotoUrl"])\n   print(profile["profileUser"]["FirstName"])\n   print(profile["profileUser"]["LastName"])\n   print(profile["profileUser"]["CompanyName"])\n   print(profile["profileUser"]["Title"])\n\nUse the rank data to get the user\'s rank and related information:\n\n.. code-block:: python\n\n   print(rank_data["RankLabel"])\n   print(rank_data["RankImageUrl"])\n   print(rank_data["EarnedPointTotal"])\n   print(rank_data["EarnedBadgeTotal"])\n   print(rank_data["CompletedTrailTotal"])\n   print(rank_data["PointTotalForNextRank"])\n   print(rank_data["BadgeTotalForNextRank"])\n\nThe list of awards contains details about each award (badge/recognition) earned by the user:\n\n.. code-block:: python\n\n   for award in awards:\n      print(award["AwardType"], award["Award"]["Label"])\n',
    'author': 'Aaron George',
    'author_email': 'angeorge.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ang3orge/trailhead-scraper',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

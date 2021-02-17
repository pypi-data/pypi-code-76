# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fittrackee',
 'fittrackee.application',
 'fittrackee.emails',
 'fittrackee.migrations',
 'fittrackee.migrations.versions',
 'fittrackee.users',
 'fittrackee.workouts']

package_data = \
{'': ['*'],
 'fittrackee': ['dist/*',
                'dist/img/*',
                'dist/img/sports/*',
                'dist/img/weather/*',
                'dist/static/css/*',
                'dist/static/js/*',
                'dist/static/media/*'],
 'fittrackee.emails': ['templates/password_reset_request/en/*',
                       'templates/password_reset_request/fr/*']}

install_requires = \
['dramatiq[redis]>=1.10.0,<2.0.0',
 'flask-bcrypt>=0.7.1,<0.8.0',
 'flask-dramatiq>=0.6.0,<0.7.0',
 'flask-migrate>=2.6,<3.0',
 'flask>=1.1,<2.0',
 'gpxpy==1.3.4',
 'gunicorn>=20.0,<21.0',
 'humanize>=3.2.0,<4.0.0',
 'psycopg2-binary>=2.8,<3.0',
 'pyjwt>=2.0,<3.0',
 'python-forecastio>=1.4,<2.0',
 'pytz>=2021.1,<2022.0',
 'shortuuid>=1.0.1,<2.0.0',
 'staticmap>=0.5.4,<0.6.0',
 'tqdm>=4.56,<5.0']

entry_points = \
{'console_scripts': ['fittrackee = fittrackee.__main__:main',
                     'fittrackee_init_data = fittrackee.__main__:init_data',
                     'fittrackee_upgrade_db = fittrackee.__main__:upgrade_db',
                     'fittrackee_worker = fittrackee.__main__:dramatiq_worker']}

setup_kwargs = {
    'name': 'fittrackee',
    'version': '0.4.5',
    'description': 'Self-hosted outdoor workout/activity tracker',
    'long_description': '# FitTrackee\n**A simple self-hosted workout/activity tracker.**  \n\n[![PyPI version](https://img.shields.io/pypi/v/fittrackee.svg)](https://pypi.org/project/fittrackee/) \n[![Python Version](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](https://python.org)\n[![Flask Version](https://img.shields.io/badge/flask-1.1-brightgreen.svg)](http://flask.pocoo.org/) \n[![code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) \n[![type check: mypy](https://img.shields.io/badge/type%20check-mypy-blue)](http://mypy-lang.org/)  \n[![React Version](https://img.shields.io/badge/react-17.0-brightgreen.svg)](https://reactjs.org/) \n[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)  \n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/290a285f22e94132904dc13b4dd19d1d)](https://www.codacy.com/app/SamR1/FitTrackee)\n[![pipeline status](https://gitlab.com/SamR1/FitTrackee/badges/master/pipeline.svg)](https://gitlab.com/SamR1/FitTrackee/-/commits/master)\n[![coverage report](https://gitlab.com/SamR1/FitTrackee/badges/master/coverage.svg)](https://gitlab.com/SamR1/FitTrackee/-/commits/master) <sup><sup>1</sup></sup>\n\n---\n\nThis web application allows you to track your outdoor activities (workouts) from gpx files and keep your data on your own server.  \nNo mobile app is developed yet, but several existing mobile apps can store workouts data locally and export them into a gpx file.  \nExamples (for Android):  \n* [Runner Up](https://github.com/jonasoreland/runnerup) (GPL v3)  \n* [ForRunners](https://gitlab.com/brvier/ForRunners) (GPL v3)  \n* [OpenTracks](https://github.com/OpenTracksApp/OpenTracks) (Apache License)  \n* [FitoTrack](https://codeberg.org/jannis/FitoTrack) (GPL v3)  \n* [AlpineQuest](https://www.alpinequest.net/) (Proprietary, no trackers according to [exodus privay report](https://reports.exodus-privacy.eu.org/en/reports/search/psyberia.alpinequest.free/))  \n\nMaps are displayed using [Open Street Map](https://www.openstreetmap.org).  \nIt is also possible to add a workout without a gpx file.\n\n**Still under heavy development (some features may be unstable).**  \n(see [issues](https://github.com/SamR1/FitTrackee/issues) and [documentation](https://samr1.github.io/FitTrackee) for more information)  \n\n![FitTrackee Dashboard Screenshot](https://samr1.github.io/FitTrackee/_images/fittrackee_screenshot-01.png)\n\n---\n\nNotes:  \n_1. Test coverage: only for Python API_\n',
    'author': 'SamR1',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamR1/FitTrackee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

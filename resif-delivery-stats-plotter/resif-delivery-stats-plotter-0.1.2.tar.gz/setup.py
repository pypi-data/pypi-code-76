# encoding: utf8
from io import open

from setuptools import find_packages, setup

with open('resif_delivery_stats_plotter/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.1.2'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = [
    'click',
    'click-log',
    'obspy',
    'requests-cache',
    'ordered_enum',
    'arrow',
    'DateTimeRange',
    'jinja2',
    'pint',
    'matplotlib',
    'pandas',
    'iso3166',
    'staticmap',
    'geopandas',
    'descartes',
    #'folium',
    #'plotly',
    #'kaleido',
]

description = '''resif-delivery-stats-plotter is a command line tool to plot statistics about requests and metadata/data deliveries
by the datacenter about a seismic network handled by Résif. This tool is mostly designed to help the seismic networks' PI
to build their annual activity reports. See http://seismology.resif.fr/'''

kwargs = {
    'name': 'resif-delivery-stats-plotter',
    'version': version,
    'description': 'Résif Delivery stats plotter',
    'long_description': readme,
    'author': 'Philippe Bollard',
    'author_email': 'philippe.bollard@univ-grenoble-alpes.fr',
    'maintainer': 'Philippe Bollard',
    'maintainer_email': 'philippe.bollard@univ-grenoble-alpes.fr',
    'url': 'https://gitlab.com/resif/resif-delivery-stats-plotter',
    'license': 'GPLv3',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    'install_requires': REQUIRES,
    'tests_require': ['coverage', 'pytest'],
    'packages': find_packages(exclude=('tests', 'tests.*')),
    'include_package_data': True,
    'entry_points': '''
        [console_scripts]
        resif-delivery-stats-plotter=resif_delivery_stats_plotter.cli:cli
    ''',

}

setup(**kwargs)
# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phl_budget_data',
 'phl_budget_data.etl',
 'phl_budget_data.etl.collections',
 'phl_budget_data.etl.collections.by_industry',
 'phl_budget_data.etl.collections.monthly',
 'phl_budget_data.etl.sentinel',
 'phl_budget_data.etl.utils']

package_data = \
{'': ['*'],
 'phl_budget_data': ['data/processed/collections/by-industry/wage/*',
                     'data/processed/collections/monthly/city/*',
                     'data/processed/collections/monthly/school/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'boto3>=1.17.12,<2.0.0',
 'click>=7.0,<8.0',
 'desert>=2020.11.18,<2021.0.0',
 'intervaltree>=3.1.0,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy==1.18.0',
 'pandas>=1.2.1,<2.0.0',
 'pdfplumber>=0.5.25,<0.6.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.3.0,<4.0.0']

entry_points = \
{'console_scripts': ['phl-monthly-collections-etl = '
                     'phl_budget_data.__main__:monthly_collections_etl',
                     'phl-update-monthly-city-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_city_collections',
                     'phl-update-monthly-school-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_school_collections',
                     'phl-update-monthly-wage-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_wage_collections']}

setup_kwargs = {
    'name': 'phl-budget-data',
    'version': '0.1.1',
    'description': 'PHL Budget Data',
    'long_description': '# phl-budget-data\n\nAggregating and cleaning City of Philadelphia budget-related data\n\n## Installation\n\n```\npip install phl_budget_data\n```\n## Examples\n\n',
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PhiladelphiaController/phl-budget-data',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

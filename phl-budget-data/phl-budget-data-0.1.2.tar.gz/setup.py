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
 'phl_budget_data': ['data/processed/collections/by-industry/birt/*',
                     'data/processed/collections/by-industry/sales/*',
                     'data/processed/collections/by-industry/wage/*',
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
{'console_scripts': ['phl-birt-collections-etl = '
                     'phl_budget_data.__main__:birt_collections_etl',
                     'phl-monthly-collections-etl = '
                     'phl_budget_data.__main__:monthly_collections_etl',
                     'phl-sales-collections-etl = '
                     'phl_budget_data.__main__:sales_collections_etl',
                     'phl-update-monthly-city-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_city_collections',
                     'phl-update-monthly-school-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_school_collections',
                     'phl-update-monthly-wage-collections = '
                     'phl_budget_data.etl.sentinel.core:update_monthly_wage_collections']}

setup_kwargs = {
    'name': 'phl-budget-data',
    'version': '0.1.2',
    'description': 'PHL Budget Data',
    'long_description': '# phl-budget-data\n\nAggregating and cleaning City of Philadelphia budget-related data\n\n# Installation\n\n```\npip install phl_budget_data\n```\n# Examples\n\nThe subsections below list examples for loading various kinds of budget-related data sets for the City of Philadelphia.\n\n## Revenue Reports\n\nData is available from the City of Philadelphia\'s Revenue reports, as published to the [City\'s website](https://www.phila.gov/departments/department-of-revenue/reports/).\n\n### City Collections\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to fiscal year (example: [FY 2021](https://www.phila.gov/documents/fy-2021-city-monthly-revenue-collections/)).\n\n\nLoad the data:\n\n```python\nfrom phl_budget_data.clean import load_monthly_tax_collections\n\ndata = load_monthly_tax_collections("city")\ndata.head()\n```\n\nOutput:\n```python\n                             name  fiscal_year        total month_name  month  fiscal_month  year       date\n0  wage_earnings_net_profits_city         2021  112703449.0        dec     12             6  2020 2020-12-01\n1       wage_earnings_net_profits         2021  149179593.0        dec     12             6  2020 2020-12-01\n2                       wage_city         2021  111383438.0        dec     12             6  2020 2020-12-01\n3                       wage_pica         2021   35437417.0        dec     12             6  2020 2020-12-01\n4                            wage         2021  146820855.0        dec     12             6  2020 2020-12-01\n```\n### School District Collections\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to fiscal year (example: [FY 2021](https://www.phila.gov/documents/fy-2021-school-district-monthly-revenue-collections/)).\n\nLoad the data:\n\n```python\nfrom phl_budget_data.clean import load_monthly_tax_collections\n\ndata = load_monthly_tax_collections("school")\ndata.head()\n```\n\nOutput:\n\n```python\n                name  fiscal_year     total month_name  month  fiscal_month  year       date\n0        real_estate         2021  30509964        dec     12             6  2020 2020-12-01\n1      school_income         2021    163926        dec     12             6  2020 2020-12-01\n2  use_and_occupancy         2021  15288162        dec     12             6  2020 2020-12-01\n3             liquor         2021   2207352        dec     12             6  2020 2020-12-01\n4       other_nontax         2021     45772        dec     12             6  2020 2020-12-01\n```\n\n### Monthly Wage Tax Collections by Industry\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to calendar year (example: [2020](https://www.phila.gov/documents/2020-wage-tax-by-industry/)).\n\n\nLoad the data:\n\n```python\nfrom phl_budget_data.clean import load_wage_collections_by_industry\n\ndata = load_wage_collections_by_industry()\ndata.head()\n```\n\nOutput:\n\n```python\n                                            industry             parent_industry       total month_name  month  fiscal_month  year  fiscal_year       date\n0                                  Other Governments                  Government    177693.0        dec     12             6  2020         2021 2020-12-01\n1                                    Social Services  Health and Social Services   4631670.0        dec     12             6  2020         2021 2020-12-01\n2  Outpatient Care Centers and Other Health Services  Health and Social Services   5302884.0        dec     12             6  2020         2021 2020-12-01\n3  Doctors, Dentists, and Other Health Practitioners  Health and Social Services   3390537.0        dec     12             6  2020         2021 2020-12-01\n4                                          Hospitals  Health and Social Services  19327622.0        dec     12             6  2020         2021 2020-12-01\n```\n\n\n## Quarterly City Manager\'s Report\n\nPDF reports are available on the City of Philadelphia\'s website [here](https://www.phila.gov/finance/reports-Quarterly.html).\n\n*Coming Soon*\n\n',
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

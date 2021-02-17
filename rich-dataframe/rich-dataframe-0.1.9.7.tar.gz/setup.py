# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_dataframe']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.2,<2.0.0', 'rich>=9.10.0,<10.0.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'rich-dataframe',
    'version': '0.1.9.7',
    'description': 'Create animated and pretty Pandas Dataframe',
    'long_description': "[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![License: Apache-2.0](https://img.shields.io/badge/Apache-2.0%20v3-blue.svg)](https://github.com/khuyentran1401/rich-dataframe/blob/master/LICENSE)\n\n# Rich DataFrame\n\nCreate animated and pretty Pandas Dataframe or Pandas Series, as shown below:\n\n![image](https://github.com/khuyentran1401/rich-dataframe/blob/master/images/prettify_table.gif?raw=True)\n\n# Installation\n```bash\npip install rich-dataframe\n```\n# Usage\n## Minimal example\n```python\nfrom sklearn.datasets import fetch_openml\nfrom rich_dataframe import prettify\n\nspeed_dating = fetch_openml(name='SpeedDating', version=1)['frame']\n\ntable = prettify(speed_dating)\n    \n```\n\nIf you want to pass a non-dataframe object, `rich_dataframe` got it covered too!\n```python \nfrom rich_dataframe import prettify\n\nvar = {'a': 1, 'b': 3}\nprettify(var)\n```\n![image](https://github.com/khuyentran1401/rich-dataframe/blob/master/images/non_dataframe.png?raw=True)\n## Parameters\n* **df: pd.DataFrame**\nThe data you want to prettify\n* **row_limit : int, optional**\n    Number of rows to show, by default `20`\n* **col_limit : int, optional**\n    Number of columns to show, by default `10`\n* **first_rows : bool, optional**\n    Whether to show first n rows or last n rows, by default `True`. If this is set to `False`, show last n rows.\n* **first_cols : bool, optional**\n    Whether to show first n columns or last n columns, by default `True`. If this is set to `False`, show last n rows.\n* **delay_time : int, optional**\n    How fast is the animation, by default `5`. Increase this to have slower animation.\n\n",
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/rich-dataframe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

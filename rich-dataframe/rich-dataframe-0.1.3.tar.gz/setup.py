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
    'version': '0.1.3',
    'description': 'Create animated and pretty Pandas Dataframe',
    'long_description': "# Rich DataFrame\n\nCreate animated and pretty Pandas Dataframe, as shown below:\n\n![image](prettify_table.gif)\n\n# Installation\n```bash\npip install rich-dataframe\n```\n# Usage\n## Minimal example\n```python\nfrom sklearn.datasets import fetch_openml\nfrom rich_dataframe import DataFramePrettify\n\nif __name__=='__main__':\n   \n    speed_dating = fetch_openml(name='SpeedDating', version=1)['frame']\n    \n    table = DataFramePrettify(speed_dating, row_limit=20, first_rows=True, delay_time=5).prettify()\n    \n```\n## Parameters\n* **df: pd.DataFrame**\nThe data you want to prettify\n* **row_limit : int, optional**\n    Number of rows to show, by default `20`\n* **col_limit : int, optional**\n    Number of columns to show, by default `10`\n* **first_rows : bool, optional**\n    Whether to show first n rows or last n rows, by default `True`. If this is set to False, show last n rows.\n* **first_cols : bool, optional**\n    Whether to show first n columns or last n columns, by default True. If this is set to `False`, show last n rows.\n* **delay_time : int, optional**\n    How fast is the animation, by default `5`. Increase this to have slower animation.\n\n",
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/rich-dataframe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.7.8',
}


setup(**setup_kwargs)

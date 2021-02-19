# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictdatabase']

package_data = \
{'': ['*']}

install_requires = \
['path-dict>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'dictdatabase',
    'version': '0.4.0',
    'description': 'Easy-to-use database using dicts',
    'long_description': '# DictDataBase\n\n[![Downloads](https://pepy.tech/badge/dictdatabase)](https://pepy.tech/project/dictdatabase)\n[![Downloads](https://pepy.tech/badge/dictdatabase/month)](https://pepy.tech/project/dictdatabase)\n[![Downloads](https://pepy.tech/badge/dictdatabase/week)](https://pepy.tech/project/dictdatabase)\n\nDictDataBase is a simple but fast and secure database for handling dicts (or PathDicts for more advanced features), that uses json files as the underlying storage mechanism.\nIt is also multiprocessind and multithreading safe, due to the employed locking mechanisms.\n\n## Import\n\n```python\n\timport DictDataBase as DDB\n```\n\n\n## Configuration\n\nThere are 3 configuration options.\nSet storage_directory to the path of the directory that will contain your database files:\n\n```python\n\tDDB.config.storage_directory = "./ddb_storage" # Default value\n```\n\nIf you want to use compressed files, set use_compression to True.\nThis will make the db files significantly smaller and might improve performance if your disk is slow.\nHowever, the files will not be human readable.\n```python\n\tDDB.config.use_compression = False # Default value\n```\n\nIf you set pretty_json_files to True, the json db files will be indented and the keys will be sorted.\nIt won\'t affect compressed files, since the are not human-readable anyways.\n```python\n\tDDB.config.pretty_json_files = True # Default value\n```\n\n\n\n\n## Create dicts\nBefore you can access dicts, you need to explicitly create them.\n\nDo create ones that already exist, this would raise an exception.\nAlso do not access ones that do not exist, this will also raise an exception.\n\n```python\n\tuser_data_dict = {\n\t\t"users": {\n\t\t\t"Ben": {\n\t\t\t\t"age": 30,\n\t\t\t\t"job": "Software Engineer"\n\t\t\t},\n\t\t\t"Sue": {\n\t\t\t\t"age": 21:\n\t\t\t\t"job": "Student"\n\t\t\t},\n\t\t\t"Joe": {\n\t\t\t\t"age": 50,\n\t\t\t\t"job": "Influencer"\n\t\t\t}\n\t\t},\n\t\t"follows": [["Ben", "Sue"], ["Joe", "Ben"]]\n\t})\n\tDDB.create("user_data", db=user_data_dict)\n\t# There is now a file called user_data.json (or user_data.ddb if you use compression)\n\t# in your specified storage directory.\n```\n\n\n## Read dicts\n```python\n\td = DDB.read("user_data")\n\t# You now have a copy of the dict named "user_data"\n\tprint(d == user_data_dict) # True\n```\n\n## Write dicts\n\n```python\n\timport DictDataBase as DDB\n\twith DDB.session("user_data") as (session, d):\n\t\t# You now have a handle on the dict named "user_data"\n\t\t# Inside the with statement, the file of user_data will be locked, and no other\n\t\t# processes will be able to interfere.\n\t\td["follows"].append(["Sue", "Ben"])\n\t\tsession.save_changes()\n\t\t# Now the changes to d are written to the database\n\n\tprint(DDB.read("user_data")["follows"])\n\t# -> [["Ben", "Sue"], ["Joe", "Ben"], ["Sue", "Ben"]]\n```\n\nIf you do not call session.save_changes(), the database file will not be modified.\n',
    'author': 'Marcel Kröker',
    'author_email': 'kroeker.marcel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkrd/DictDataBase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

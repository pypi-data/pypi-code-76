# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sql_metadata']
install_requires = \
['sqlparse>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'sql-metadata',
    'version': '1.11.0',
    'description': 'Uses tokenized query returned by python-sqlparse and generates query metadata',
    'long_description': '# sql-metadata\n\n[![PyPI](https://img.shields.io/pypi/v/sql_metadata.svg)](https://pypi.python.org/pypi/sql_metadata)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://github.com/macbre/sql-metadata/graphs/commit-activity)\n[![Downloads](https://pepy.tech/badge/sql-metadata/month)](https://pepy.tech/project/sql-metadata)\n\nUses tokenized query returned by [`python-sqlparse`](https://github.com/andialbrecht/sqlparse) and generates query metadata.\n**Extracts column names and tables** used by the query. Provides a helper for **normalization of SQL queries** and **tables aliases resolving**.\n\nSupported queries syntax:\n\n* MySQL\n* PostgreSQL\n* [Apache Hive](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DML)\n\n## Usage\n\n```\npip install sql-metadata\n```\n\n```python\n>>> import sql_metadata\n\n>>> sql_metadata.get_query_tokens("SELECT * FROM foo")\n[<DML \'SELECT\' at 0x7F14FFDEB808>, <Wildcard \'*\' at 0x7F14FFDEB940>, <Keyword \'FROM\' at 0x7F14FFDEBBB0>, <Name \'foo\' at 0x7F14FFDEB9A8>]\n\n>>> sql_metadata.get_query_columns("SELECT test, id FROM foo, bar")\n[u\'test\', u\'id\']\n\n>>> sql_metadata.get_query_tables("SELECT a.* FROM product_a.users AS a JOIN product_b.users AS b ON a.ip_address = b.ip_address")\n[\'product_a.users\', \'product_b.users\']\n\n>>> sql_metadata.get_query_columns("INSERT /* VoteHelper::addVote xxx */  INTO `page_vote` (article_id,user_id,`time`) VALUES (\'442001\',\'27574631\',\'20180228130846\')")\n[\'article_id\', \'user_id\', \'time\']\n\n>>> sql_metadata.get_query_columns("SELECT a.* FROM product_a.users AS a JOIN product_b.users AS b ON a.ip_address = b.ip_address")\n[\'a.*\', \'a.ip_address\', \'b.ip_address\']\n\n>>> sql_metadata.get_query_tables("SELECT test, id FROM foo, bar")\n[u\'foo\', u\'bar\']\n\n>>> sql_metadata.get_query_limit_and_offset(\'SELECT foo_limit FROM bar_offset LIMIT 50 OFFSET 1000\')\n(50, 1000)\n\n>>> sql_metadata.get_query_limit_and_offset(\'SELECT foo_limit FROM bar_offset limit 2000,50\')\n(50, 2000)\n\n>>> sql_metadata.get_query_table_aliases("SELECT test FROM foo AS f")\n{\'f\': \'foo\'}\n```\n\n> See `test/test_query.py` file for more examples of a bit more complex queries.\n\n### Queries normalization\n\n```python\n>>> from sql_metadata import generalize_sql\n>>> generalize_sql(\'SELECT /* Test */ foo FROM bar WHERE id in (1, 2, 56)\')\n\'SELECT foo FROM bar WHERE id in (XYZ)\'\n```\n\n> See `test/test_normalization.py` file for more examples of a bit more complex queries.\n\n## Stargazers over time\n\n[![Stargazers over time](https://starchart.cc/macbre/sql-metadata.svg)](https://starchart.cc/macbre/sql-metadata)\n',
    'author': 'Maciej Brencz',
    'author_email': 'maciej.brencz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/macbre/sql-metadata',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

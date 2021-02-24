# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynch',
 'asynch.proto',
 'asynch.proto.columns',
 'asynch.proto.compression',
 'asynch.proto.settings',
 'asynch.proto.streams',
 'asynch.proto.utils']

package_data = \
{'': ['*']}

install_requires = \
['ciso8601', 'clickhouse-cityhash', 'leb128', 'lz4', 'pytz', 'tzlocal', 'zstd']

setup_kwargs = {
    'name': 'asynch',
    'version': '0.1.3',
    'description': 'A asyncio driver for ClickHouse with native tcp protocol',
    'long_description': '# asynch\n\n![pypi](https://img.shields.io/pypi/v/asynch.svg?style=flat)\n![license](https://img.shields.io/github/license/long2ice/asynch)\n![workflows](https://github.com/long2ice/asynch/workflows/pypi/badge.svg)\n![workflows](https://github.com/long2ice/asynch/workflows/ci/badge.svg)\n\n## Introduction\n\n`asynch` is an asyncio ClickHouse Python Driver with native (TCP) interface support, which reuse most of [clickhouse-driver](https://github.com/mymarilyn/clickhouse-driver) and comply with [PEP249](https://www.python.org/dev/peps/pep-0249/).\n\n## Install\n\n```shell\n> pip install asynch\n```\n\n## Usage\n\nConnect to ClickHouse\n\n```python\nfrom asynch import connect\n\nasync def connect_database():\n    conn = await connect(\n        host = "127.0.0.1",\n        port = 9000,\n        database = "default",\n        user = "default",\n        password = "",\n    )\n```\n\nCreate table by sql\n\n```python\nasync def create_table():\n    async with conn.cursor(cursor=DictCursor) as cursor:\n        await cursor.execute(\'create database if not exists test\')\n        await cursor.execute("""\n        CREATE TABLE if not exists test.asynch\n            (\n                `id`       Int32,\n                `decimal`  Decimal(10, 2),\n                `date`     Date,\n                `datetime` DateTime,\n                `float`    Float32,\n                `uuid`     UUID,\n                `string`   String,\n                `ipv4`     IPv4,\n                `ipv6`     IPv6\n\n            )\n            ENGINE = MergeTree\n                ORDER BY id"""\n        )\n```\n\nUse `fetchone`\n\n```python\nasync def fetchone():\n    async with conn.cursor() as cursor:\n        await cursor.execute("SELECT 1")\n        ret = cursor.fetchone()\n        assert ret == (1,)\n```\n\nUse `fetchmany`\n\n```python\nasync def fetchall():\n    async with conn.cursor() as cursor:\n        await cursor.execute("SELECT 1")\n        ret = cursor.fetchall()\n        assert ret == [(1,)]\n```\n\nUse `DictCursor` to get result with dict\n\n```python\nasync def dict_cursor():\n    async with conn.cursor(cursor=DictCursor) as cursor:\n        await cursor.execute("SELECT 1")\n        ret = cursor.fetchall()\n        assert ret == [{"1": 1}]\n```\n\nInsert data with dict\n\n```python\nfrom asynch.cursors import DictCursor\n\nasync def insert_dict():\n    async with conn.cursor(cursor=DictCursor) as cursor:\n        ret = await cursor.execute(\n            """INSERT INTO test.asynch(id,decimal,date,datetime,float,uuid,string,ipv4,ipv6) VALUES""",\n            [\n                {\n                    "id": 1,\n                    "decimal": 1,\n                    "date": "2020-08-08",\n                    "datetime": "2020-08-08 00:00:00",\n                    "float": 1,\n                    "uuid": "59e182c4-545d-4f30-8b32-cefea2d0d5ba",\n                    "string": "1",\n                    "ipv4": "0.0.0.0",\n                    "ipv6": "::",\n                }\n            ],\n        )\n        assert ret == 1\n```\n\nInsert data with tuple\n\n```python\nasync def insert_tuple():\n    async with conn.cursor(cursor=DictCursor) as cursor:\n        ret = await cursor.execute(\n            """INSERT INTO test.asynch(id,decimal,date,datetime,float,uuid,string,ipv4,ipv6) VALUES""",\n            [\n                (\n                    1,\n                    1,\n                    "2020-08-08",\n                    "2020-08-08 00:00:00",\n                    1,\n                    "59e182c4-545d-4f30-8b32-cefea2d0d5ba",\n                    "1",\n                    "0.0.0.0",\n                    "::",\n                )\n            ],\n        )\n        assert ret == 1\n```\n\nUse connection pool\n\n```python\nasync def use_pool():\n    pool = await asynch.create_pool()\n    async with pool.acquire() as conn:\n        async with conn.cursor() as cursor:\n            await cursor.execute("SELECT 1")\n            ret = cursor.fetchone()\n            assert ret == (1,)\n    pool.close()\n    await pool.wait_closed()\n```\n\n## ThanksTo\n\n- [clickhouse-driver](https://github.com/mymarilyn/clickhouse-driver), ClickHouse Python Driver with native interface support.\n\n## License\n\nThis project is licensed under the [Apache-2.0](https://github.com/long2ice/asynch/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/asynch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

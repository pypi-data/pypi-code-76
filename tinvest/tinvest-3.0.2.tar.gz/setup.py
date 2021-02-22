# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinvest', 'tinvest.cli']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'pydantic>=1.2,<2', 'requests>=2.22,<3.0']

extras_require = \
{'cli': ['typer>=0.3.2,<1'],
 'orjson': ['orjson>=3.4'],
 'uvloop': ['uvloop>=0.15']}

entry_points = \
{'console_scripts': ['tinvest = tinvest.cli.app:app']}

setup_kwargs = {
    'name': 'tinvest',
    'version': '3.0.2',
    'description': 'Tinkoff Invest',
    'long_description': '# T-Invest\n\n[![Build Status](https://api.travis-ci.com/daxartio/tinvest.svg?branch=master)](https://travis-ci.com/daxartio/tinvest)\n[![PyPI](https://img.shields.io/pypi/v/tinvest)](https://pypi.org/project/tinvest/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinvest)](https://www.python.org/downloads/)\n[![Codecov](https://img.shields.io/codecov/c/github/daxartio/tinvest)](https://travis-ci.com/daxartio/tinvest)\n[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/tinvest)](https://github.com/daxartio/tinvest)\n[![Tinvest](https://img.shields.io/github/stars/daxartio/tinvest?style=social)](https://github.com/daxartio/tinvest)\n\n```\npip install tinvest\n```\n\nДанный проект представляет собой инструментарий на языке Python для работы с OpenAPI Тинькофф Инвестиции, который можно использовать для создания торговых роботов.\n\nКлиент предоставляет синхронный и асинхронный API для взаимодействия с Тинькофф Инвестиции.\n\nЕсть возможность делать запросы через командную строку, подробнее [тут](https://daxartio.github.io/tinvest/cli/).\n\n```\npip install tinvest[cli]\n\n# Пример использования\ntinvest openapi --token TOKEN portfolio\n```\n\nPerformance.\n\n```\npip install tinvest[uvloop]\npip install tinvest[orjson]\n```\n\n## Начало работы\n\n### Где взять токен аутентификации?\n\nВ разделе инвестиций вашего [личного кабинета tinkoff](https://www.tinkoff.ru/invest/). Далее:\n\n* Перейдите в настройки\n* Проверьте, что функция "Подтверждение сделок кодом" отключена\n* Выпустите токен для торговли на бирже и режима "песочницы" (sandbox)\n* Скопируйте токен и сохраните, токен отображается только один раз, просмотреть его позже не получится, тем не менее вы можете выпускать неограниченное количество токенов\n\n## Документация\n\n[tinvest](https://daxartio.github.io/tinvest/)\n\n[invest-openapi](https://tinkoffcreditsystems.github.io/invest-openapi/)\n\n### Быстрый старт\n\nДля непосредственного взаимодействия с OpenAPI нужно создать клиента. Клиенты разделены на streaming и rest.\n\nПримеры использования SDK находятся [ниже](#Примеры).\n\n### У меня есть вопрос\n\n[Основной репозиторий с документацией](https://github.com/TinkoffCreditSystems/invest-openapi/) — в нем вы можете задать вопрос в Issues и получать информацию о релизах в Releases.\nЕсли возникают вопросы по данному SDK, нашёлся баг или есть предложения по улучшению, то можно задать его в Issues.\n\n## Примеры\n\nДля работы с данным пакетом вам нужно изучить [OpenAPI Тинькофф Инвестиции](https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/)\n\n### Streaming\n\nПредоставляет асинхронный интерфейс.\n\n> При сетевых сбоях будет произведена попытка переподключения.\n\n```python\nimport asyncio\nimport tinvest as ti\n\n\nasync def main():\n    async with ti.Streaming(\'TOKEN\') as streaming:\n        await streaming.candle.subscribe(\'BBG0013HGFT4\', ti.CandleResolution.min1)\n        await streaming.orderbook.subscribe(\'BBG0013HGFT4\', 5)\n        await streaming.instrument_info.subscribe(\'BBG0013HGFT4\')\n        async for event in streaming:\n            print(event)\n\n\nasyncio.run(main())\n```\n\n### Синхронный REST API Client\n\nДля выполнения синхронных http запросов используется библиотека `requests`.\nС описанием клиентов можно ознакомиться по этой [ссылке](https://daxartio.github.io/tinvest/tinvest/clients/).\n\n```python\nimport tinvest\n\nTOKEN = "<TOKEN>"\n\nclient = tinvest.SyncClient(TOKEN)\n\nresponse = client.get_portfolio()  # tinvest.PortfolioResponse\nprint(response.payload)\n```\n\n```python\n# Handle error\n...\nclient = tinvest.SyncClient(TOKEN)\n\ntry:\n    response = client.get_operations("", "")\nexcept tinvest.BadRequestError as e:\n    print(e.response)  # tinvest.Error\n```\n\n### Асинхронный REST API Client\n\nДля выполнения асинхронных http запросов используется библиотека `aiohttp`.\nКлиенты имеют такой же интерфейс как в синхронной реализации, за исключением того,\nчто функции возвращают объект корутина.\n\n```python\nimport asyncio\nimport tinvest\n\nTOKEN = "<TOKEN>"\n\n\nasync def main():\n    client = tinvest.AsyncClient(TOKEN)\n    response = await client.get_portfolio()  # tinvest.PortfolioResponse\n    print(response.payload)\n\n    await client.close()\n\nasyncio.run(main())\n```\n\n### Sandbox\n\nSandbox позволяет вам попробовать свои торговые стратегии, при этом не тратя реальные средства. Протокол взаимодействия полностью совпадает с Production окружением.\n\n```python\nclient = tinvest.AsyncClient(SANDBOX_TOKEN, use_sandbox=True)\n# client = tinvest.SyncClient(SANDBOX_TOKEN, use_sandbox=True)\n```\n\n## Environments\n\n| name                  | required | default |\n|-----------------------|:--------:|--------:|\n| TINVEST_TOKEN         | optional |      \'\' |\n| TINVEST_SANDBOX_TOKEN | optional |      \'\' |\n| TINVEST_USE_ORJSON    | optional |    True |\n| TINVEST_USE_UVLOOP    | optional |    True |\n\n## Contributing\n\nПредлагайте свои пулл реквесты, проект с открытым исходным кодом.\n',
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/tinvest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

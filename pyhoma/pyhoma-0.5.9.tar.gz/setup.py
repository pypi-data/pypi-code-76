# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhoma']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.1,<4.0.0', 'backoff>=1.10.0,<2.0.0', 'pyhumps>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'pyhoma',
    'version': '0.5.9',
    'description': 'Async Python wrapper to interact with internal Somfy TaHoma API',
    'long_description': '# Somfy TaHoma\n\n<p align=center>\n    <a href="https://github.com/iMicknl/python-tahoma-api/actions"><img src="https://github.com/iMicknl/python-tahoma-api/workflows/CI/badge.svg"/></a>\n    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>\n</p>\n\nAn updated and async version of the original [tahoma-api](https://github.com/philklei/tahoma-api) by [@philklei](https://github.com/philklei). The aim of this wrapper is to offer an easy to consume Python wrapper for the internal API\'s used by tahomalink.com.\n\nSomfy TaHoma has an official API, which can be consumed via the [Somfy-open-api](https://github.com/tetienne/somfy-open-api). Unfortunately only a few device classes are supported via the official API, thus the need for this wrapper.\n\nThis package is written for the Home Assistant [ha-tahoma](https://github.com/iMicknl/ha-tahoma) integration, but could be used by any Python project interacting with Somfy TaHoma devices.\n\n## Installation\n\n```bash\npip install pyhoma\n```\n\n## Getting started\n\n```python\nimport asyncio\nimport time\n\nfrom pyhoma.client import TahomaClient\n\nUSERNAME = ""\nPASSWORD = ""\n\nasync def main() -> None:\n    async with TahomaClient(USERNAME, PASSWORD) as client:\n        try:\n            await client.login()\n        except Exception as exception:  # pylint: disable=broad-except\n            print(exception)\n            return\n\n        devices = await client.get_devices()\n\n        for device in devices:\n            print(f"{device.label} ({device.id}) - {device.controllable_name}")\n            print(f"{device.widget} - {device.ui_class}")\n\n        while True:\n            events = await client.fetch_events()\n            print(events)\n\n            time.sleep(2)\n\nasyncio.run(main())\n```\n\n## Development\n\n### Installation\n\n- For Linux, install [pyenv](https://github.com/pyenv/pyenv) using [pyenv-installer](https://github.com/pyenv/pyenv-installer)\n- For MacOS, run `brew install pyenv`\n- Don\'t forget to update your `.bashrc` file (or similar):\n  ```\n  export PATH="~/.pyenv/bin:$PATH"\n  eval "$(pyenv init -)"\n  ```\n- Install the required [dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)\n- Install [poetry](https://python-poetry.org): `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`\n\n- Clone this repository\n- `cd python-tahoma-api`\n- Install the required Python version: `pyenv install`\n- Init the project:\xa0`poetry install`\n- Run `poetry run pre-commit install`\n\n## PyCharm\n\nAs IDE you can use [PyCharm](https://www.jetbrains.com/pycharm/).\n\nUsing snap, run `snap install pycharm --classic` to install it.\n\nFor MacOS, run `brew cask install pycharm-ce`\n\nOnce launched, don\'t create a new project, but open an existing one and select the **python-tahoma-api** folder.\n\nGo to _File | Settings | Project: nre-tag | Project Interpreter_. Your interpreter must look like `<whatever>/python-tahoma-api/.venv/bin/python`\n',
    'author': 'Mick Vleeshouwer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iMicknl/python-tahoma-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

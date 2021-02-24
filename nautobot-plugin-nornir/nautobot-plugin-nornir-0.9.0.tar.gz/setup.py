# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_plugin_nornir',
 'nautobot_plugin_nornir.plugins.credentials',
 'nautobot_plugin_nornir.plugins.inventory',
 'nautobot_plugin_nornir.tests',
 'nautobot_plugin_nornir.tests.inventory']

package_data = \
{'': ['*']}

install_requires = \
['nautobot>=1.0.0-alpha.1,<2.0.0', 'nornir-nautobot>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'nautobot-plugin-nornir',
    'version': '0.9.0',
    'description': 'Nautobot Nornir plugin.',
    'long_description': '# ntc-nautobot-plugin-nornir\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot).\n\n## Installation\n\nThe plugin is available as a Python package in pypi and can be installed with pip\n```shell\npip install nautobot-plugin-nornir\n```\n\n> The plugin is compatible with Nautobot 1.0.0 and higher\n \nTo ensure Nautobot Nornir Plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot_nornir` package:\n\n```no-highlight\n# echo nautobot-plugin-nornir>> local_requirements.txt\n```\n\nOnce installed, the plugin needs to be enabled in your `configuration.py`\n```python\n# In your configuration.py\nPLUGINS = ["nautobot_nornir"]\n\nPLUGINS_CONFIG = {\n  "nautobot_nornir": {\n    "nornir_settings": {\n      "credentials": "nautobot_nornir.credentials.env_vars.CredentialsEnvVars",\n      "nornir.core": {"num_workers": 10},\n      "runner": {\n        "plugin": "threaded",\n        "options": {\n            "num_workers": 10,\n        },\n      },\n    },\n  }\n```\n\nThe plugin behavior can be controlled with the following list of settings\n\n- TODO\n\n## Usage\n\n### API\n\nTODO\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n### CLI Helper Commands\n\nThe project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. \n\nEach command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`\n\n#### Local dev environment\n```\n  build            Build all docker images.\n  debug            Start Nautobot and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  restart          Restart Nautobot and its dependencies.\n  start            Start Nautobot and its dependencies in detached mode.\n  stop             Stop Nautobot and its dependencies.\n```\n\n#### Utility \n```\n  cli              Launch a bash shell inside the running Nautobot container.\n  create-user      Create a new user in django (default: admin), will prompt for password.\n  makemigrations   Run Make Migration in Django.\n  nbshell          Launch a nbshell session.\n```\n#### Testing \n\n```\n  bandit           Run bandit to validate basic static code security analysis.\n  black            Run black to check that Python files adhere to its style standards.\n  flake8           This will run flake8 for the specified name and Python version.\n  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.\n  pylint           Run pylint code analysis.\n  tests            Run all tests for this plugin.\n  unittest         Run Django unit tests for the plugin.\n```\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n\n## Screenshots\n\nTODO\n\n## Initial very basic usage\n\n```\nfrom nornir import InitNornir\n\nPLUGIN_SETTINGS = {\n    "inventory": "nautobot_nornir.inventory.nautobot_orm.NautobotORMInventory",\n    "credentials": "nautobot_nornir.credentials.env_vars.CredentialsEnvVars",\n    "nornir.core": {"num_workers": 10},\n    "inventory_params" : {\n        "use_fqdn": True,\n        "fqdn": "example.com",\n    },\n}\n\nnornir = InitNornir(\n    core=PLUGIN_SETTINGS.get("nornir.core"),\n    logging={"enabled": False},\n    inventory={\n        "plugin": PLUGIN_SETTINGS.get("inventory"),\n        "options": {\n            "credentials_class": PLUGIN_SETTINGS.get("credentials"),\n            "params": PLUGIN_SETTINGS.get("inventory_params"),\n            "queryset": self.queryset,\n        },\n    },\n)\n```\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-nornir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

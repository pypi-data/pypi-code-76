# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_nautobot',
 'nornir_nautobot.plugins',
 'nornir_nautobot.plugins.inventory',
 'nornir_nautobot.plugins.processors',
 'nornir_nautobot.plugins.tasks.dispatcher',
 'nornir_nautobot.plugins.tasks.dispatcher.utils',
 'nornir_nautobot.utils']

package_data = \
{'': ['*']}

install_requires = \
['nornir-jinja2>=0.1.1,<0.2.0',
 'nornir-napalm>=0.1.1,<0.2.0',
 'nornir-netmiko>=0.1.1,<0.2.0',
 'nornir-utils>=0.1.1,<0.2.0',
 'nornir>=3.0.0,<4.0.0',
 'pynautobot>=1.0.1,<2.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'nornir.plugins.inventory': ['NautobotInventory = '
                              'nornir_nautobot.plugins.inventory.nautobot:NautobotInventory']}

setup_kwargs = {
    'name': 'nornir-nautobot',
    'version': '1.0.0',
    'description': 'Nornir Nautobot',
    'long_description': '# nornir_nautobot\n\n## Overview\n\nThe nornir_nautobot project intends to solve two primary use cases.\n\n* Providing a Nornir inventory that leverages Nautobot\'s API.\n* A set of opinionated Nornir plugins.\n\nThe set of plugins intended to provide mechanisms to include common networking workflows that will help enable network automation. As\nas example, there are method to get configurations or test network connectivity. Over time this will include functions to perform\nactions such as get vlans, neighbors, protocols, etc.\n\n## Getting Started\n\n```shell\npip install nornir-nautobot\n```\n\n### \n\nTo get started without a configuration file:\n\n```python\n    nornir_obj = InitNornir(\n        inventory={\n            "plugin": "NautobotInventory",\n            "options": {\n                "nautobot_url": os.getenv("NAUTOBOT_URL"),\n                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),\n                "ssl_verify": False,\n            },\n        },\n    )\n```\n\n1. As part of the initialization of the Nornir object, include the inventory key\n2. Set the plugin to the name of `NautobotInventory`\n3. Set the required options (if not already set via environment variables)\n\nAccepted options include:\n\n| Option            | Parameter         | Value                                                                                 | Default             |\n| ----------------- | ----------------- | ------------------------------------------------------------------------------------- | ------------------- |\n| Nautobot URL      | nautobot_url      | String - The base url of Nautobot (`http://localhost:8000` or `https://nautobot_url`) | env(NAUTOBOT_URL)   |\n| Nautobot Token    | nautobot_token    | String - The token to authenticate to Nautobot API                                    | env(NAUTOBOT_TOKEN) |\n| SSL Verify        | ssl_verify        | Boolean - True or False to verify SSL                                                 | True                |\n| Filter Parameters | filter_parameters | Dictionary - Key/value pairs corresponding to Nautobot API searches                   | {}                  |\n\n\n## Testing\n\nIn the early stages of testing since pynautobot is not available in a public state yet, it will be included via the `tests/packages` directory. This is **not** intended to be part of the actual packaging when things go live.\n\n## Construct\n\nPynautobot will provide for the basic information that is required for Nornir to be able to leverage the inventory. The pynautobot object will also be made available at `host.data.pynautobot_object` to be able to access information provided from the _dcim devices_ endpoint.\n\n\n## Task Plugins\n\nThe only task plugin currently is the "dispatcher" plugin. This plugin dispatches to the more specific OS specific functions. To demonstrate the primary components of the code:\n\n#### Dispatcher Sender\n\n```python\n    try:\n        driver_task = getattr(driver_class, method)\n    except AttributeError:\n        logger.log_failure(obj, f"Unable to locate the method {method} for {driver}")\n        raise NornirNautobotException()\n\n    result = task.run(task=driver_task, *args, **kwargs)\n```\n\n#### Dispatcher Receiver\n\n```python\nclass NautobotNornirDriver:\n    """Default collection of Nornir Tasks based on Napalm."""\n\n    @staticmethod\n    def get_config(task: Task, backup_file: str, *args, **kwargs) -> Result:\n```\n\n#### Calling Dispatcher\n\n```python\ntask.run(\n    task=dispatcher,\n    name="SAVE BACKUP CONFIGURATION TO FILE",\n    method="get_config",\n    obj=obj,\n    logger=logger,\n    backup_file=backup_file,\n    remove_lines=global_settings,\n    substitute_lines=substitute_lines,\n)\n```\n\nThe dispatcher expects the two primary objects, the `obj` and `logger` objects. The `obj` object should be a Device model instance. The logger should be `NornirLogger` instance which is imported from `nornir_nautobot.utils.logger`. This logging object optionally takes in a Nautobot job_result object. This is for use within the Nautobot platform Jobs. \n\nEach task will raise a `NornirNautobotException` for known issues. Using a custom processor, the user can predict when it was an well known error.\n\n## Processor Plugins\n\nProvided for convenience within the `nornir_nautobot.plugins.processors` is the `BaseProcessor` and `BaseLoggingProcessor` as boilerplate code for creating a custom processor.\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nautobot.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_chatops',
 'nautobot_chatops.api',
 'nautobot_chatops.api.views',
 'nautobot_chatops.dispatchers',
 'nautobot_chatops.management.commands',
 'nautobot_chatops.migrations',
 'nautobot_chatops.tests',
 'nautobot_chatops.tests.workers',
 'nautobot_chatops.workers']

package_data = \
{'': ['*'], 'nautobot_chatops': ['static/nautobot/*', 'templates/nautobot/*']}

install_requires = \
['nautobot',
 'nautobot-capacity-metrics',
 'pyjwt[crypto]>=1.7.1,<2.0.0',
 'slackclient>=2.7.1,<3.0.0',
 'texttable>=1.6.2,<2.0.0',
 'webexteamssdk>=1.3,<2.0']

entry_points = \
{'nautobot.workers': ['clear = nautobot_chatops.workers.clear:clear',
                      'nautobot = nautobot_chatops.workers.nautobot:nautobot']}

setup_kwargs = {
    'name': 'nautobot-chatops',
    'version': '1.0.0',
    'description': 'A plugin providing chatbot capabilities for Nautobot',
    'long_description': '# nautobot-chatops\n\nA multi-platform ChatOps bot plugin for [Nautobot](https://github.com/nautobot/nautobot).\n\n- Support for multiple chat platforms (currently Slack, Microsoft Teams, and WebEx Teams)\n- Write a command once and run it on every supported platform, including rich content formatting\n- Extensible - other Nautobot plugins can provide additional commands which will be dynamically discovered.\n- Automatic generation of basic help menus (accessed via `help`, `/command help`, or `/command sub-command help`)\n- Metrics of command usage via the `nautobot_capacity_metrics` plugin.\n\n## Installation\n\nThe plugin is available as a Python package in pypi and can be installed with pip\n```shell\npip install nautobot-chatops\n```\n\n> The plugin is compatible with Nautobot 1.0.0beta1 and higher\n\nOnce installed, the plugin needs to be enabled in your `nautobot_config.py`\n```python\n# In your nautobot_config.py\nPLUGINS = ["nautobot_chatops"]\n\nPLUGINS_CONFIG = {\n    "nautobot_chatops": {\n         #     ADD YOUR SETTINGS HERE\n    }\n}\n```\n\nNautobot supports `Slack`, `MS Teams` and `Webex Teams` as backends but by default all of them are disabled. You need to explicitly enable the chat platform(s) that you want to use in the `PLUGINS_CONFIG` with one or more of `enable_slack`, `enable_ms_teams` or `enable_webex_teams`. \n\nThe plugin behavior can be controlled with the following list of general settings:\n\n| Configuration Setting        | Description | Mandatory? | Default |\n| ---------------------------- | ----------- | ---------- | ------- |\n| `delete_input_on_submission` | After prompting the user for additional inputs, delete the input prompt from the chat history | No | `False` |\n\nFor details on the platform-specific settings needed to enable Nautobot for the chat platform(s) of your choice, refer to [the documentation](docs/chat_setup.md).\n\n## Documentation\n\n- [Installation Guide](docs/chat_setup.md)\n- [Design](docs/design.md)\n- [Contributing](docs/contributing.md)\n- [FAQ](docs/FAQ.md)\n\n## Contributing\n\nThank you for your interest in helping to improve Nautobot!\nRefer to the [contributing guidelines](docs/contributing.md) for details.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](docs/FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #nautobot).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-nautobot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cogwatch']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.5,<2.0', 'watchgod==0.7']

entry_points = \
{'console_scripts': ['example = runner:__poetry_run']}

setup_kwargs = {
    'name': 'cogwatch',
    'version': '2.1.0',
    'description': 'Automatic hot-reloading for your discord.py command files.',
    'long_description': '<h1 align="center">Cog Watch</h1>\n    \n<div align="center">\n  <strong><i>Automatic hot-reloading for your discord.py command files.</i></strong>\n  <br>\n  <br>\n  \n  <a href="https://pypi.org/project/cogwatch">\n    <img src="https://img.shields.io/pypi/v/cogwatch?color=0073B7&label=Latest&style=for-the-badge" alt="Version" />\n  </a>\n  \n  <a href="https://python.org">\n    <img src="https://img.shields.io/pypi/pyversions/cogwatch?color=0073B7&style=for-the-badge" alt="Python Version" />\n  </a>\n</div>\n<br>\n\n### Getting Started\n`cogwatch` is a utility that you can plug into your `discord.py` bot that will watch your command files directory *(cogs)* \nand automatically reload them as you modify or move them around in real-time. No more manually reloading commands with \nother commands, or *(worse yet)* restarting your bot, every time you edit that embed!\n\nYou can install the library with `pip install cogwatch`.\n\nImport the `watch` decorator and apply it to your `on_ready` method and let the magic take effect.\n\n```python\nimport asyncio\nfrom discord.ext import commands\nfrom cogwatch import watch\n\n\nclass ExampleBot(commands.Bot):\n    def __init__(self):\n        super().__init__(command_prefix=\'!\')\n\n    @watch(path=\'commands\')\n    async def on_ready(self):\n        print(\'Bot ready.\')\n\n    async def on_message(self, message):\n        if message.author.bot:\n            return\n\n        await self.process_commands(message)\n\n\nasync def main():\n    client = ExampleBot()\n    await client.start(\'YOUR_TOKEN_GOES_HERE\')\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n**NOTE:** `cogwatch` will only run if the **\\_\\_debug\\_\\_** flag is set on Python. You can read more about that \n[here](https://docs.python.org/3/library/constants.html). In short, unless you run Python with the *-O* flag from\nyour command line, **\\_\\_debug\\_\\_** will be **True**. If you just want to bypass this feature, pass in `debug=False` and\nit won\'t matter if the flag is enabled or not.\n\n#### Using a Classless Bot\nIf you are using a classless bot you cannot use the decorator method and instead must manually create your watcher.\n\n```python\nfrom discord.ext import commands\nfrom cogwatch import Watcher\n\nclient = commands.Bot(command_prefix=\'!\')\n\n\n@client.event\nasync def on_ready():\n    print(\'Bot ready.\')\n\n    watcher = Watcher(client, path=\'commands\')\n    await watcher.start()\n\n\nclient.run(\'YOUR_TOKEN_GOES_HERE\')\n```\n\n### Configuration\nYou can pass any of these values to the decorator:\n\n**path=\'commands\'**: Root name of the cogs directory; cogwatch will only watch within this directory -- recursively.\n\n**debug=True**: Whether to run the bot only when the Python **\\_\\_debug\\_\\_** flag is True. Defaults to True.\n\n**loop=None**: Custom event loop. Defaults to the current running event loop.\n\n**default_logger=True**: Whether to use the default logger *(to sys.stdout)* or not. Defaults to True.\n\n**preload=False**: Whether to detect and load all found cogs on start. Defaults to False.\n\n### Logging\nBy default, the utility has a logger configured so users can get output to the console. You can disable this by\npassing in `default_logger=False`. If you want to hook into the logger -- for example, to pipe your output to another\nterminal or `tail` a file -- you can set up a custom logger like so:\n\n```python\nimport logging\nimport sys\n\nwatch_log = logging.getLogger(\'cogwatch\')\nwatch_log.setLevel(logging.INFO)\nwatch_handler = logging.StreamHandler(sys.stdout)\nwatch_handler.setFormatter(logging.Formatter(\'[%(name)s] %(message)s\'))\nwatch_log.addHandler(watch_handler)\n```\n\n-----\n\nCheck out my other discord.py utility: **[dpymenus](https://github.com/robertwayne/dpymenus)** -- *Simplified menus for discord.py developers.*\n',
    'author': 'Rob Wagner',
    'author_email': '13954303+robertwayne@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robertwayne/cogwatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pluploader',
 'pluploader.confluence',
 'pluploader.confluence.jobs',
 'pluploader.mpac',
 'pluploader.upm',
 'pluploader.util']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'click_default_group>=1.2.2,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'configargparse>=1.2.3,<2.0.0',
 'furl>=2.1.0,<3.0.0',
 'html5lib>=1.1,<2.0',
 'importlib-metadata>=1.7.0,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'packaging>=20.4,<21.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=9.5.1,<10.0.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.9']}

entry_points = \
{'console_scripts': ['pluploader = pluploader.main:main']}

setup_kwargs = {
    'name': 'pluploader',
    'version': '0.7.0',
    'description': 'CLI Confluence/Jira Plugin uploader',
    'long_description': '<!-- markdownlint-configure-file\n{\n  "no-bare-urls": false,\n  "no-trailing-punctuation": false,\n  "line-length": false\n}\n-->\n\n# pluploader\n\n![PyPI version](https://img.shields.io/pypi/v/pluploader?style=flat-square) ![Upload Python Package](https://img.shields.io/github/workflow/status/livelyapps/pluploader/Python%20package/master?style=flat-square)\n\n![pluploader](.github/images/pluploader-demo-1.gif)\n\nA advanced command-line plugin uploader/installer/manager for atlassian\nserver and cloud instances (Confluence/Jira) written in python(3).\n\n## Installation\n\nRegulary tested on Linux (Arch Linux), MacOS and Windows 10.\n\n### pip (recommended)\n\n```bash\npip3 install pluploader\n```\n\n### brew (MacOS)\n\n```bash\nbrew tap craftamap/tap && brew install pluploader\n```\n\n### Docker\n\nIf you do not want to install python3 or pip, you can also pull the latest\ndocker image from dockerhub or github:\n\n```bash\ndocker pull craftamap/pluploader:latest\n# OR\ndocker pull docker.pkg.github.com/livelyapps/pluploader/pluploader:latest\n```\n\npluploader can then be run by executing\n\n```bash\ndocker run -v "$(pwd)":/workdir -it craftamap/pluploader:v0.6.0\n```\n\n## Usage\n\nFor a in-depth explanation, see `pluploader --help`\n\n> ℹ This documentation describes the master branch, and not (necessarily) the latest release.\n\n### Global Options\n\nYou can specify various global options:\n\n- `--base-url <base-url>`, default: `http://localhost:8090`\n- `--user <username>`, default: `admin`\n- `--password <password>`, default: `admin`  \n  If you do not want to put your password in the command line plaintext, you can\n  also use...\n- `--ask-for-password`\n\nAll Global Options can be overwritten by using a configuration file. See more in\n[Configuration](#Configuration)\n\n### Configuration\n\nIf you don\'t want to write the username or password (or any other global\nparameter) each time, you can use a filed called `.pluprc`, either placed in\nyour current maven project or/and in your home directory. A example looks like\nthis:\n\n```bash\nbase_url: https://example.com:8090\nuser: admin\npassword: admin\n```\n\n### Environment variables\n\nYou can also specify username, password and base url by using `PLUP_USER`,\n`PLUP_PASSWORD` and `PLUP_BASEURL`.\n\n### Uploading plugins\n\nIf you are in a maven project, the basic usage is fairly simple. Just type:\n\n```bash\npluploader --user admin --password admin\n```\n\nThe pluploader then uploads and enables the current artifact specified in the\npom.xml\n\nIf you are not in a maven directory currently, but you want to upload a specific\nfile, you can also use the `-f plugin.jar` flag.\n\nIf you want to confirm your upload, you can also use the `-i` /\n`--interactive` flag.\n\nIt is recommended to use the pluploader with maven. The usage looks like:\n\n```bash\natlas-mvn clean package && pluploader\n```\n\n#### Installing apps from the marketplace\n\n![Uploading  gifs](.github/images/pluploader-demo-3.gif)\n\npluploader supports downloading apps from the atlassian marketplace to your local\nmachine and installing them afterwards. You need to supply either `--mpac-key`,\nwhich is the normal addon-key, or `--mpac-id` (experimental), which is the\nnumeric id of an marketplace id (72307 https://marketplace.atlassian.com/apps/72307)\n\n```bash\npluploader --mpac-key com.atlassian.confluence.extra.team-calendars\n```\n\n**NOTE**:\nIf you specify one of the global options, you need to add the `install`-command:\n\n```bash\npluploader --base-url https://your-confluence.com:8090 install\n```\n\nYou can work around this by using the configuration file or by using environment variables.\n\n### Installing a connect descriptor to a cloud instance.\n\n\n![Uploading to cloud](.github/images/pluploader-demo-5.gif)\n\npluploader also supports installing atlassian-connect plugins to cloud instances\nby enabling cloud support with `--cloud` and providing the descriptor url with `--plugin-uri`.\n\n```bash\npluploader install --cloud --plugin-uri https://your.ngrok.here\n```\n\n### Managing plugins\n\n![Managing plugins](.github/images/pluploader-demo-2.gif)\n\npluploader can also replace the usage of the universal plugin manager completely\nby using the subcommands `list`, `info`, `enable`, `disable`, and `uninstall`\n(`enable` and `disable` are not supported in the atlassian cloud).\n\nTo get a list of all installed plugins of the configured instance, just type:\n\n```bash\npluploader list\n```\n\nA green checkmark indicates that the plugin is enabled, while a exclamation mark\nindicates that the plugin is disabled.\n\nIn order to retrieve more information about a specific plugin, you can use the\ncommand `info`.\n\n```bash\npluploader info com.example.plugin.key\n```\n\nThe plugin key can be omitted in a maven directory, if the parameter\n`atlassian.plugin.key` is set in plaintext.\n\nThe commands `enable`, `disable` or `uninstall` follow the same syntax.\n\n### Safe Mode\n\npluploader also supports disabling or enabling all apps using Safe Mode (does not work in cloud).\n\nTo retrieve the status if safe-mode is enabled at the moment, use\n\n```bash\npluploader safe-mode status\n```\n\nYou can enable and disable safe mode by using\n\n```bash\npluploader safe-mode enable\n```\n\nAnd\n\n```bash\npluploader safe-mode disable\n# OR\npluploader safe-mode disable --keep-state\n```\n\n### Licenses\n\n![Licenses Gif](.github/images/pluploader-demo-4.gif)\n\nYou can also use the pluploader to get and set licenses for your plugins.\n\nTo get the current license information:\n\n```bash\npluploader license info com.example.plugin.key\n```\n\nTo set a lciense, use the `update` functionality.\n\n```bash\npluploader license update com.example.plugin.key --license "AAA..."\n```\n\n> ℹ Pro tip: Use `xargs` to read a license from a file by using\n>\n> ```bash\n> cat license.txt | xargs pluploader license update --license\n> ```\n\nYou can also apply [timebomb licenses](https://developer.atlassian.com/platform/marketplace/timebomb-licenses-for-testing-server-apps/)\n\nby using\n\n```bash\npluploader license timebomb com.example.plugin.key --timebomb threehours\n```\n\nYou can choose between 3 hours (threehours), 60 seconds (sixtyseconds) and\n10 seconds (tenseconds)\n\nTo remove an applied license, you can use:\n\n```bash\npluploader license delete com.example.plugin.key\n```\n\n### API\n\nYou can interact with the HTTP/REST-API of your configured instance by using\n`pluploader api ENDPOINT [BODY]`. The arguments work a bit like the\nwell-known tool `curl`. You can use `-X METHOD` to choose the HTTP method and\n`-H "HEADER-NAME: HEADER-VALUE"` to add a HTTP header.\n\n```bash\npluploader api -X POST -H "content-type: application/json" rest/api/content/ \'{ "type":"page", "title":"My Test Page", "space":{"key":"TEST"}, "body":{ "storage": { "value":"<p>This is a new page</p>", "representation":"storage" } } }\'\n```\n\n### RPC\n\n`pluploader rpc` allows interaction with the (deprecated, but  still\nfunctional) confluence rpc api by providing the method name and it\'s\nrequired arguments. You do not need to care about the rpc-authentication,\nas this command takes care of it. Therefore, you can also obmit the first\nparameter (String token) required for many commands.\n\n\n```bash\npluploader rpc addUser \'{"name":"charlie", "fullname": "charlie", "email":"charlie@charlie"}\' charlie\n```\n\n### Scheduled Jobs (Confluence - Experimental)\n\n> ℹ This feature is currently experimental and only works in specific version of\n> Confluence (tested on Confluence 7.5).\n\nPluploader can also be used to retrieve information about confluence jobs and\nexecute them.\n\nYou can grab a list of all jobs by running\n\n```bash\npluploader job list\n```\n\nAvailable options are:\n\n- `--hide-default` - Hides confluence internal jobs\n- `--print-all-infos` - print more informations\n\nYou can also run jobs by running\n\n```bash\npluploader job run\n```\n\nGet more information about a job by running\n\n```bash\npluploader job info\n```\n\nAnd disable or enable jobs by running\n\n```bash\npluploader job enable\n# AND\npluploader job disable\n```\n\nA job can be specified by either using `--id <job id>` or by using\n`--idx <job index in list>`. If no job is specified, you will be asked\ninteractively.\n\n\n## Development\n\npluploader uses [poetry](https://python-poetry.org/) as it\'s package manager. As a command line argument parser, [Typer](https://typer.tiangolo.com/) is used.\n\n## FAQ\n\n### Why would I use the pluploader over X?\n\nOf course, you can use whatever tool you want to.\n\n### Why would I use the pluploader over the UPM?\n\nIt\'s a faster workflow.\n\n### Why would I use the pluploader over the Atlas-CLI?\n\natlas-cli is awesome, but sadly it\'s deprecated. Also since you can use your own\nmaven command with pluploader, you therefore can skip tests, make a mvn clean,\nand many more.\n\nIn general, pluploader is just a bit more flexiable.\n\n### Why would I use the pluploader over QuickReload?\n\nQuickReload is cool, but some of us prefer to use docker instances or atlas-standalone\nrather than atlas-run.\n',
    'author': 'Fabian Siegel',
    'author_email': 'fabian@livelyapps.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/livelyapps/pluploader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centralcli', 'centralcli.cli_levels']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'Pygments>=2.7.3,<3.0.0',
 'aiohttp>=3.7.3,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'certifi>=2020.12.5,<2021.0.0',
 'colorama>=0.4.4,<0.5.0',
 'halo>=0.0.31,<0.0.32',
 'idna>=2.10,<3.0',
 'pendulum>=2.1.2,<3.0.0',
 'pycentral>=0.0.1,<0.0.2',
 'pylibyaml>=0.1.0,<0.2.0',
 'rich>=9.10.0,<10.0.0',
 'shellingham>=1.3.2,<2.0.0',
 'tablib>=3.0.0,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tinydb>=4.3.0,<5.0.0',
 'typer>=0.3.2,<0.4.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['cencli = centralcli.cli:app']}

setup_kwargs = {
    'name': 'centralcli',
    'version': '0.4a19',
    'description': 'A CLI for interacting with Aruba Central (Cloud Management Platform).  Facilitates bulk imports, exports, reporting.  A handy tool if you have devices managed by Aruba Central.',
    'long_description': "# Aruba Central API CLI\n\n---\n\nA CLI app for interacting with Aruba Central Cloud Management Platform. With cross-platform / shell support. i.e. Bash, zsh, PowerShell, etc.\n\n`TODO [demo](docs/media/demo.gif)`\n\n## Features\n- Cross Platform Support\n- Auto Completion\n- Specify device, site, etc. by fuzzy match of multiple fields (i.e. name, mac, serial#, ip address)\n- multiple output formats\n- output to file\n- multiple account support (easily switch between different central accounts)\n- Batch Operation based on data from input file.  i.e. Add sites in batch based on data from a csv.\n\n## Installation\nRequires python3 and pip\n\n`pip3 install centralcli`\n\n> You can also install in a virtual environment (venv), but you'll lose auto-completion, unless you activate the venv.\n\n## Configuration\n\nRefer to [config.yaml.example](config/config.yaml.example) to guide in the creation of config.yaml and place in the config directory.\n\nCentralCli will look in \\<Users home dir\\>/.config/centralcli, and \\<Users home dir\\>/.centralcli.\ni.e. on Windows `c:\\Users\\wade\\.centralcli` or on Linux `/home/wade/.config/centralcli`\n\nOnce `config.yaml` is populated per [config.yaml.example](config/config.yaml.example), run some test commands to validate the config.\n\nExample test command `cencli show all`\n\n```bash\nwade@wellswa6:~ $\xa0cli show all\n✔ Collecting Data [monitoring/v1/switches]\n✔ Collecting Data [monitoring/v2/aps]\n✔ Collecting Data [monitoring/v1/gateways]\nname               ip               mac            model                 group          site     serial      type     labels       version                status\n-----------------  ---------------  -------------  --------------------  -------------  -------  ----------  -------  -----------  ---------------------  --------\nBR1_315_0c:88      10.101.6.200/24  --redacted--   315                   Branch1        Antigua  -redacted-  ap       Branch View  8.7.1.1_78245          Up\nIAP305             10.2.30.102      --redacted--   305                   TemplateGroup           -redacted-  ap                    6.5.1.0-4.3.1.2_58595  Down\nLABAP4             10.0.30.233/24   --redacted--   345                   WadeLab                 -redacted-  ap                    8.7.1.0_77203          Down\nsw-zippity                          --redacted--   J9773A                WadeLab                 -redacted-  SW                    16.10.000x             Down\nsw-ConsolePi-dev   10.0.10.154      --redacted--   Aruba2930F-(JL258A)   WadeLab        WadeLab  -redacted-  SW                    16.10.0011             Down\n2930F-Branch1      10.101.5.4       --redacted--   Aruba2930F-(JL258A)   Branch1        Antigua  -redacted-  SW       Branch View  16.10.0007             Up\n6200F-Bot          10.0.40.16       --redacted--   6200F 48G-(JL728A)    WadeLab        WadeLab  -redacted-  CX                    10.06.0010             Up\nSDBranch1:7008     192.168.240.101  --redacted--   A7008                 Branch1        Antigua  -redacted-  gateway  Branch View  8.5.0.0-2.0.0.6_76205  Up\nVPNC1              192.168.30.201   --redacted--   A7005                 WadeLab        WadeLab  -redacted-  gateway  Branch View  8.6.0.4-2.2.0.3_77966  Up\nVPNC2              192.168.30.202   --redacted--   A7005                 WadeLab        WadeLab  -redacted-  gateway  Branch View  8.6.0.4-2.2.0.3_77966  Up\n...\n\n```\n\nUse cencli --help to become familiar with the command options.\n> *NOTE:* Aruba Central API CLI is still evolving.  Structure and the format of outputs are likely to change over time.\n\n### Auto Completion\nThe CLI supports auto-completion.  To configure auto-completion run `cencli --install-completion`.  This will auto-detect the type of shell you are running in, and install the necessary completion into your profile.  You'll need to exit the shell and start a new session for it to take effect.\n\n## Usage Notes:\n\n### Caching & Friendly identifiers\n- Caching: The CLI caches information on all devices, sites, groups, and templates in Central.  It's a minimal amount per device, and is done to allow human friendly identifiers.  The API typically accepts serial #, site id, etc.  This function allows you to specify a dev for example by name, IP, mac (any format), and serial.\nThe lookup sequence for a device:\n\n    1. Exact Match of any of the identifier fields (name, ip, mac, serial)\n    2. case insensitive match\n    3. case insensitive match disregarding all hyphens and underscores (in case you type 6200f_bot and the device name is 6200F-Bot)\n    4. Case insensitive Fuzzy match with implied wild-card, otherwise match any devices that start with the identifier provided. `cencli show switches 6200F` will result in a match of `6200F-Bot`.\n\n> If there is no match found, a cache update is triggered in most scenarios, and the match rules are re-tried.  The cache is also updated every 3 hours (if you run a command and it's older than 3 hours, it will update the cache first).  This update 3 hour update will be removed in a future release once auto-update/retry is implemented for all identifier types (groups, and templates currently lack the update/retry bit)\n\n- Caching works in a similar manner for groups, templates, and sites.  Sites can match on name and nearly any address field.  So if you only had one site in San Antonio you could specify that site with `show sites 'San Antonio'`  \\<-- Note the use of quotes because there is a space in the name.\n\n- **Multiple Matches**:  It's possible to specify an identifier that returns multiple matches (if drops all the way down to the Fuzzy match/implied trailing wild-card).  If that occurs you are prompted to select the intended device from a list of the matches.\n\n### Output Formats\n\nThere are a number of output formats available.  Most commands default to what is likely the easiest to view given the number of fields.  Otherwise longer outputs are typically displayed vertically by default.  If the output can reasonably fit, it's displayed in tabular format horizontally.\n\nYou can specify the output format with command line flags `--json`, `--yaml`, `--csv`, `--rich`  rich is tabular format with folding (multi line within the same row) and truncating.\n\n> Most outputs will evolve to support an output with the most commonly desired fields by default and expanded vertical output via the `-v` option (not implemented yet.)\n\n### File Output\n\nJust use --out \\<filename\\> (or \\<path\\\\filename\\>), and specify the desired format.\n\n## CLI Tree\n\nUse `--help`, which you can do at any level.  `cli --help`, `cli do --help` etc.  A Tree will be documented here once it's built out more.\n",
    'author': 'Wade Wells (Pack3tL0ss)',
    'author_email': 'wade@consolepi.org',
    'maintainer': 'Wade Wells (Pack3tL0ss)',
    'maintainer_email': 'wade@consolepi.org',
    'url': 'https://github.com/Pack3tL0ss/central-api-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

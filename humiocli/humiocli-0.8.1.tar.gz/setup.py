# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['humiocli']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.8.0,<3.0.0',
 'chardet>=4.0.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'humioapi>=0.8.2,<0.9.0',
 'pandas>=1.1.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pygments>=2.6.1,<3.0.0',
 'pytz>=2018.9,<2019.0',
 'snaptime>=0.2.4,<0.3.0',
 'structlog>=20.2.0,<21.0.0',
 'tabulate>=0.8.8,<0.9.0',
 'tzlocal>=2.1,<3.0']

entry_points = \
{'console_scripts': ['hc = humiocli.cli:cli']}

setup_kwargs = {
    'name': 'humiocli',
    'version': '0.8.1',
    'description': 'Command line interface for interacting with the Humio API using the humioapi library',
    'long_description': '# Do things with the Humio API from the command line\n\n> This project requires `Python>=3.6.1`\n\nThis is a companion CLI to the unofficial [humioapi](https://github.com/gwtwod/humioapi) library. It lets you use most of its features easily from the command line. If you\'re looking for the official CLI it can be found [here: humiolib](https://github.com/humio/python-humio).\n\n## Installation\n\n```bash\npython3 -m pip install humiocli\n# or even better\npipx install humiocli\n```\n\n## Main features\n\n* Streaming searches with several output formats\n* Subsearches (pipe output from one search into a new search)\n* Defaults configured through ENV variables (precedence: `shell options` > `shell environment` > `config-file`)\n* Splunk-like chainable relative time modifiers\n* Switch easily from browser to CLI by passing the search URL to urlsearch\n* Ingest data to Humio (but you should use Filebeat for serious things)\n* List repositories\n\n## First time setup\n\nStart the guided setup wizard to configure your environment\n\n```bash\nhc wizard\n```\n\nThis will help you create an environment file with a default Humio URL and token, so you don\'t have to explicitly provide them as options later.\n\nAll options may be provided by environment variables on the format\n`HUMIO_<OPTION>=<VALUE>`. If a .env file exists in `~/.config/humio/.env` it\nwill be automatically sourced on execution without overwriting the\nexisting environment.\n\n## Examples\n\n### Execute a search in all repos starting with `reponame` and output `@rawstring`s\n\n```bash\nhc search --repo \'reponame*\' \'#type=accesslog statuscode>=400\'\n```\n\n### Execute a search using results with fields from another search ("subsearch")\n\n#### Step 1: Set the output format to `or-fields`\n\n```bash\nhc search --repo=auth \'username | select([session_id, app_name])\' --outformat=or-fields | jq \'.\'\n```\n\nThis gives a JSON-structure with prepared search strings from all field-value combinations. The special field `SUBSEARCH` combines all search strings for all fields.\n\nExample output:\n\n```json\n{\n  "session_id": "\\"session_id\\"=\\"5CF4A111\\" or \\"session_id\\"=\\"14C8BCEA\\"",\n  "app_name": "\\"app_name\\"=\\"frontend\\"",\n  "SUBSEARCH": "(\\"session_id\\"=\\"5CF4A111\\" or \\"session_id\\"=\\"14C8BCEA\\") and (\\"app_name\\"=\\"frontend\\")"\n}\n```\n\n#### Step 2: Pipe this result to a new search and reference the desired fields:\n\n```bash\nhc search --repo=auth \'username | select([session_id, app_name])\' --outformat=or-fields | hc --repo=frontend \'#type=accesslog {{session_id}}\'\n```\n\n### Output aggregated results as ND-JSON events\n\nSimple example:\n\n> _Humios bucketing currently creates partial buckets in both ends depending on search period. You may want to provide a rounded start and stop to ensure we only get whole buckets._\n\n```bash\nhc search --repo \'sandbox*\' --start=-60m@m --stop=@m "#type=accesslog | timechart(span=1m, series=statuscode)"\n```\n\nOr with a longer multiline search\n\n```bash\nhc search --repo \'sandbox*\' --start -60m@m --stop=@m  "$(cat << EOF\n#type=accesslog\n| case {\n    statuscode<=400 | status_ok := 1 ;\n    statuscode=4*  | status_client_error := "client_error" ;\n    statuscode=5*  | status_server_error := "server_error" ;\n    * | status_broken := 1\n}\n| bucket(limit=50, function=[count(as="count"), count(field=status_ok, as="ok"), count(field=status_client_error, as="client_error"), count(field=status_server_error, as="server_error")])\n| error_percentage := (((client_error + server_error) / count) * 100)\nEOF\n)"\n```\n\n### Upload a parser file to the destination repository, overwriting any existing parser\n\n```bash\nhc makeparser --repo=\'sandbox*\' customjson\n```\n\n### Ingest a single-line log file with an ingest-token associated with a parser\n\n```bash\nhc ingest customjson\n```\n\n### Ingest a multi-line file with a user provided record separator (markdown headers) and parser\n\n```bash\nhc ingest README.md --separator \'^#\' --fields \'{"#repo":"sandbox", "#type":"markdown", "@host":"localhost"}\'\n```\n\n## Development\n\nTo install the cli and api packages in editable mode:\n\n```bash\ngit clone https://github.com/gwtwod/humiocli.git\npoetry install\n```\n\n## Create self-contained executables for easy distribution\n\nThis uses [Shiv](https://github.com/linkedin/shiv) to create a `zipapp`. A single self-contained file with all python dependencies and a shebang.\n\nOn first run, this will unpack the required modues to `~/.shiv/hc/` which will cause a short delay in startup. Subsequent runs should be fast however. The location can be controlled with the env variable `SHIV_ROOT`. You should probably clean this directory once in a while, since a new one is created every time the distributable changes.\n\n```bash\npip install shiv\nshiv -c hc -o hc humiocli -p "/usr/bin/env python3"\n```\n',
    'author': 'Jostein Haukeli',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gwtwod/humiocli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

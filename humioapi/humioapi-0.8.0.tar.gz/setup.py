# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['humioapi']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=4.0.0,<5.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pendulum>=2.1.2,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'snaptime>=0.2.4,<0.3.0',
 'structlog>=20.1.0,<21.0.0',
 'tqdm>=4.54.1,<5.0.0',
 'tzlocal>=2.1,<3.0']

setup_kwargs = {
    'name': 'humioapi',
    'version': '0.8.0',
    'description': 'An unofficial Python library wrapping the official humiolib to provide extra helpers and utility functions',
    'long_description': '# Humio API (unofficial lib)\n\n> 💡 This project requires `Python>=3.6.1`\n\n> 💡 This is not the official Humio library. It can be found [here: humiolib](https://github.com/humio/python-humio).\n\nThis is an unofficial library for interacting with [Humio](https://www.humio.com/)\'s API. This library mostly exists now because the official library was too basic back in 2019 when I first needed this. Currently this library is just a wrapper around `humiolib` to implement some convenient and opinionated helpers.\n\n## Installation\n\n```bash\npip install humioapi\n```\n\n## Main features/extensions\n\n* CLI companion tool `hc` available at [humiocli](https://github.com/gwtwod/humiocli).\n* Monkeypatched QueryJobs with a `poll_safe` method that can return or raise warnings.\n* Relative time modifiers similar to Splunk (`-7d@d` to start at midnight 7 days ago). Can also be chained (`-1d@h-30m`). [Source](https://github.com/zartstrom/snaptime).\n* List repository details (*NOTE*: normal Humio users cannot see repos without read permission).\n* Easy env-variable based configuration.\n* Create and update parsers.\n\n## Usage\n\nFor convenience your Humio URL and tokens should be set in the environment variables `HUMIO_BASE_URL` and `HUMIO_TOKEN`.\nThese can be set in `~/.config/humio/.env` and loaded through `humioapi.humio_loadenv()`, which loads all `HUMIO_`-prefixed\nvariables found in the env-file.\n\n## Query repositories\n\nCreate an instance of HumioAPI to get started\n\n```python\nimport humioapi\nimport logging\nhumioapi.initialize_logging(level=logging.INFO, fmt="human")\n\napi = humioapi.HumioAPI(**humioapi.humio_loadenv())\nrepositories = api.repositories()\n```\n\n## Iterate over syncronous streaming searches sequentially\n\n```python\nimport humioapi\nimport logging\nhumioapi.initialize_logging(level=logging.INFO, fmt="human")\n\napi = humioapi.HumioAPI(**humioapi.humio_loadenv())\nstream = api.streaming_search(\n    query="",\n    repo=\'sandbox\',\n    start="-1week@day",\n    stop="now"\n)\nfor event in stream:\n    print(event)\n```\n\n## Create pollable QueryJobs with results, metadata and warnings (raised by default)\n\n```python\nimport humioapi\nimport logging\nhumioapi.initialize_logging(level=logging.INFO, fmt="human")\n\napi = humioapi.HumioAPI(**humioapi.humio_loadenv())\nqj = api.create_queryjob(query="", repo="sandbox", start="-7d@d")\n\nresult = qj.poll_safe(raise_warnings=False)\nif result.warnings:\n    print("Oh no!", result.warnings)\nprint(result.metadata)\n```\n\n## Jupyter Notebook\n\n```python\npew new --python=python36 humioapi\n# run the following commands inside the virtualenv\npip install git+https://github.com/gwtwod/humioapi.git\npip install ipykernel seaborn matplotlib\npython -m ipykernel install --user --name \'python36-humioapi\' --display-name \'Python 3.6 (venv humioapi)\'\n```\n\nStart the notebook by running `jupyter-notebook` and choose the newly created kernel when creating a new notebook.\n\nRun this code to get started:\n\n```python\nimport humioapi\nimport logging\nhumioapi.initialize_logging(level=logging.INFO, fmt="human")\n\napi = humioapi.HumioAPI(**humioapi.humio_loadenv())\nresults = api.streaming_search(query="", repo="sandbox", start="@d", stop="now")\nfor i in results:\n    print(i)\n```\n\nTo get a list of all readable repositories with names starting with \'frontend\':\n\n```python\nrepos = sorted([k for k,v in api.repositories().items() if v[\'read_permission\'] and k.startswith(\'frontend\')])\n```\n\nMaking a timechart (lineplot):\n\n```python\n%matplotlib inline\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport pandas as pd\n\nsns.set(color_codes=True)\nsns.set_style(\'darkgrid\')\n\nresults = api.streaming_search(query=" | timechart()", repos=["sandbox"], start=start, stop=stop)\ndf = pd.DataFrame(results)\ndf[\'_count\'] = df[\'_count\'].astype(float)\n\ndf[\'_bucket\'] = pd.to_datetime(df[\'_bucket\'], unit=\'ms\', origin=\'unix\', utc=True)\ndf.set_index(\'_bucket\', inplace=True)\n\ndf.index = df.index.tz_convert(\'Europe/Oslo\')\ndf = df.pivot(columns=\'metric\', values=\'_count\')\n\nsns.lineplot(data=df)\n```\n\n## SSL and proxies\n\nAll HTTP traffic is done through `humiolib` which currently uses `requests` internally. You can probably use custom certificates with the env variable `REQUESTS_CA_BUNDLE`, or pass extra argument as `kwargs` to the various API functions.\n',
    'author': 'Jostein Haukeli',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gwtwod/humioapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runrestic', 'runrestic.metrics', 'runrestic.restic', 'runrestic.runrestic']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.0,<4.0', 'requests', 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['runrestic = runrestic.runrestic.runrestic:runrestic']}

setup_kwargs = {
    'name': 'runrestic',
    'version': '0.5.20',
    'description': 'A wrapper script for Restic backup software that inits, creates, prunes and checks backups',
    'long_description': '![python version](https://img.shields.io/badge/python-3.6+-blue.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Travis (.com)](https://api.travis-ci.com/sinnwerkstatt/runrestic.svg?branch=master)\n![PyPI](https://img.shields.io/pypi/v/runrestic)\n[![Stackshare: runrestic](https://img.shields.io/badge/stackshare-runrestic-068DFE.svg)](https://stackshare.io/runrestic)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/runrestic)\n\n# Runrestic\n\nrunrestic is a simple Python wrapper script for the\n[Restic](https://restic.net/) backup software that initiates a backup,\nprunes any old backups according to a retention policy, and validates backups\nfor consistency. The script supports specifying your settings in a declarative\nconfiguration file rather than having to put them all on the command-line, and\nhandles common errors.\n\n## Example config\n\n```toml\nrepositories = [\n    "/tmp/restic-repo",\n    "sftp:user@host:/srv/restic-repo",\n    "s3:s3.amazonaws.com/bucket_name"\n    ]\n\n[environment]\nRESTIC_PASSWORD = "CHANGEME"\n\n[backup]\nsources = [\n    "/home",\n    "/var"\n    ]\n\n[prune]\nkeep-last =  3\nkeep-hourly =  5\n```\n\nFor a more comprehensive example see the [example.toml](https://github.com/sinnwerkstatt/runrestic/blob/master/sample/example.toml)\n or check the [schema.json](https://github.com/sinnwerkstatt/runrestic/blob/master/runrestic/runrestic/schema.json)\n\n## Getting started\n\n### Installing runrestic and restic\nTo install **runrestic**, run the following command to download and install it:\n\n```bash\nsudo pip3 install --upgrade runrestic\n```\n\n<br>\n\nYou can either manually download and install [Restic](https://restic.net/) or you can just run `runrestic` and it\'ll try to download it for you.\n\n\n### Initializing and running\n\nOnce you have `restic` and `runrestic` ready, you should put a config file in on of the scanned locations, namely:\n\n- /etc/runrestic.toml\n- /etc/runrestic/*example*.toml\n- ~/.config/runrestic/*example*.toml\n\nAfterwards, run \n\n```bash\nrunrestic init # to initialize all the repos in `repositories`\n\nrunrestic  # without actions will do: runrestic backup prune check\n# or\nrunrestic [action]\n```\n\n<br>\nCertain `restic` flags like `--dry-run/-n` are built into `runrestic` as well and will be passed to restic where applicable.\n\nIf, however, you need to pass along arbitrary other flags you can now add them to the end of your `runrestic` call like so: \n```bash\nrunrestic backup -- --one-file-system\n``` \n\n### Prometheus / Grafana metrics\n[@d-matt](https://github.com/d-matt) created a nice dashboard for Grafana here: https://grafana.com/grafana/dashboards/11064/revisions\n\n### systemd timer or cron\n\nIf you want to run runrestic automatically, say once a day, the you can\nconfigure a job runner to invoke it periodically.\n\n\n#### systemd\n\nIf you\'re using systemd instead of cron to run jobs, download the [sample systemd service file](https://raw.githubusercontent.com/sinnwerkstatt/runrestic/master/sample/systemd/runrestic.service)\nand the [sample systemd timer file](https://raw.githubusercontent.com/sinnwerkstatt/runrestic/master/sample/systemd/runrestic.timer).\nThen, from the directory where you downloaded them:\n\n```bash\nsudo mv runrestic.service runrestic.timer /etc/systemd/system/\nsudo systemctl enable runrestic.timer\nsudo systemctl start runrestic.timer\n```\n\n#### cron\n\nIf you\'re using cron, download the [sample cron file](https://raw.githubusercontent.com/sinnwerkstatt/runrestic/master/sample/cron/runrestic).\nThen, from the directory where you downloaded it:\n\n```bash\nsudo mv runrestic /etc/cron.d/runrestic\nsudo chmod +x /etc/cron.d/runrestic\n```\n\n## Changelog\n* v**0.5**! Expect breaking changes.\n    * metrics output is a bit different\n    * see new `parallel` and `retry_*` options. \n\n\n## Development\n\nThis project is managed with [poetry](https://python-poetry.org/)\n\n[Install it](https://github.com/python-poetry/poetry#installation) if not already present:\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n# or\npip install --user poetry\n```\n\n### Installing dependencies\n```bash\npoetry install\n```\n\n### Running Tests\n\n```bash\npoetry run pytest\n```\n\n# Thanks\nThis project was initially based on [borgmatic](https://github.com/witten/borgmatic/) but has since evolved into something else.\n',
    'author': 'Andreas Nüßlein',
    'author_email': 'andreas@nuessle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sinnwerkstatt/runrestic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

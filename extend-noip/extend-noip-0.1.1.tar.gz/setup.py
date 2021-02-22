# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extend_noip']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.11.0,<0.12.0',
 'chardet>=4.0.0,<5.0.0',
 'logzero>=1.6.3,<2.0.0',
 'more_itertools>=8.7.0,<9.0.0',
 'pydantic[dotenv]>=1.7.3,<2.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pyquery>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['extend-noip = extend_noip.__main__:main']}

setup_kwargs = {
    'name': 'extend-noip',
    'version': '0.1.1',
    'description': 'Extend noip dns records for one more month',
    'long_description': "# extend-noip\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/extend-noip.svg)](https://badge.fury.io/py/extend-noip)\n\nExtend dns expiry date on noip.com\n\n## Automate dns/domain on noip.com\n[中文读我.md](https://github.com/ffreemt/extend-noip/blob/master/读我.md)\n\n*   Fork this repo.\n*   Set the resultant repo `Secrets`: NOIP_USERNAME's value to `your-noip-username/email`, NOIP_PASSWORD's value to `your-noip-password`\n*   [Optionally] Change `crontab` in line 6 of `.github/workflows/schedule-extend-noip.yml` to your like. (This online crontab editor may come handy [https://crontab.guru/#0_0_*/9_*_*](https://crontab.guru/#0_0_*/9_*_*))\n\n\n## Installtion\n\n```bash\npip install extend-noip\n```\nor clone [https://github.com/ffreemt/extend-noip](https://github.com/ffreemt/extend-noip) and install from the repo.\n\n## Usage\n### Supply noip `username` and `password` from the command line:\n```bash\npython -m extend-noip -u your_noip_username -p password\n```\nor use directly the ``extend-noip`` script:\n```bash\nextend-noip -u your_noip_username -p password\n```\n\n### Use environment variables `NOIP_USERNAME` and `NOIP_PASSWORD`\n*   Set username/password from the command line:\n\t```bash\n\tset NOIP_USERNAME=your_noip_username  # export in Linux or iOS\n\tset NOIP_PASSWORD=password\n\t```\n*   Or set username/password  in .env, e.g.,\n\t```bash\n\t# .env\n\tNOIP_USERNAME=your_noip_username\n\tNOIP_USERNAME=password\n\nRun `extend-noip` or `python -m  extend_noip`:\n\n```bash\nextend-noip\n```\n\nor\n\n```bash\npython -m extend_noip\n```\n\n### Check information only\n\n```bash\nextend-noip -i\n```\n\nor\n\n```bash\npython -m extend_noip -i\n```\n\n###  Print debug info\n\n```bash\nextend-noip -d\n```\n\nor\n\n```bash\npython -m extend_noip -d\n```\n\n### Brief Help\n\n```bash\nextend-noip --helpshort\n```\n\nor\n\n```bash\npython -m extend_noip --helpshort\n```\n\n### Turn off Headless Mode (Show the browser in action)\n\nYou can configure `NOIP_HEADFUL`, `NOIP_DEBUG` and `NOIP_PROXY` in the `.env` file in the working directory or any of its parent directoreis. For example,\n\n```bash\n# .env\nNOIP_HEADFUL=1\nNOIP_DEBUG=true\n# NOIP_PROXY\n```\n\n### Automation via Github Actions\n\nIt's straightforward to setup `extend-noip` to run via Github Actions, best with an infrequent crontab.\n*   Fork this repo\n*   Setup `Actions secrets` via `Settings/Add repository secrets`:\n\n|Name | Value |\n|--    | --    |\n|NOIP_USERNAME:| your_noip_username|\n|NOIP_PASSWORD:| your_noip_password |\n\nFor example, in `.github/workflows/schedule-extend-noip.yml`\n```bash\nname: schedule-extend-noip\n\non:\n  push:\n  schedule:\n    - cron: '10,40 3 */9 * *'\n...\nsetup, e.g. pip install -r requirements.txt or\npoetry install --no-dev\n...\n\n      - name: Testrun\n        env:\n          NOIP_USERNAME: ${{ secrets.NOIP_USERNAME }}\n          NOIP_PASSWORD: ${{ secrets.NOIP_PASSWORD }}\n        run: |\n          python -m extend_noip -d -i\n\n```\n\n<!---\n['158.101.140.77 Last Update 2021-02-22 02:34:45 PST',\n '168.138.222.163 Last Update 2021-02-22 03:40:55 PST']\n\n['158.101.140.77 Last Update 2021-02-22 08:39:49 PST',\n '168.138.222.163 Last Update 2021-02-22 08:40:01 PST']\n\n--->",
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/extend-noip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

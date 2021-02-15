# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dp2rathena']

package_data = \
{'': ['*'], 'dp2rathena': ['db/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'tortilla>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['dp2rathena = dp2rathena.cli:dp2rathena']}

setup_kwargs = {
    'name': 'dp2rathena',
    'version': '0.3.3',
    'description': 'Convert Divine-Pride API data to rAthena YAML',
    'long_description': '# dp2rathena: Divine-Pride API to rAthena\n\n[![PyPI - Version](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dp2rathena)](https://pypi.org/project/dp2rathena/)\n[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)\n[![codecov](https://codecov.io/gh/Latiosu/dp2rathena/branch/master/graph/badge.svg?token=B7G9O57UR8)](https://codecov.io/gh/Latiosu/dp2rathena)\n\nConvert Divine-Pride API data to rAthena DB formats.\n\nCurrently supported formats are:\n- `item_db.yml`\n- `mob_skill_db.txt`\n- (future) `mob_db.txt`\n\n## Requirements\n\n* Python 3.6+\n\n## Installation\n\n```\npip install dp2rathena\n```\n\n## Usage\n\nA [divine-pride.net](https://www.divine-pride.net/) API key is required, create an account and generate a key if you don\'t have one yet.\n\n```bash\n# Store API key\ndp2rathena config\n\n# Convert items with ids 501 and 1101\ndp2rathena item 501 1101\n\n# Convert mob skills from mob ids in a newline separated file\ndp2rathena mobskill -f my_mobs.txt\n\n# Print out help text\ndp2rathena -h\n```\n\n## Limitations\n\nAll fields are mapped except the ones listed below:\n\n### `item_db.yml`\n\n**Partially Mapped**\n- `"Type"` - when the item type is "Consumable" on DP and subtype "Special", we output a few possible options for user to choose the correct one (Healing, Usable, DelayConsume or Cash)\n- `"SubType"` - when the item type is "Ammo" on DP, we output all rathena ammo subtypes for user to choose correct option as DP doesn\'t map all rathena ammo subtypes\n\n**Not Mapped** _(insufficient data)_\n- `"Script"` / `"EquipScript"` / `"UnEquipScript"` - script to execute when some action is performed with the item\n- `"Class"` - upper class types that can equip item\n- `"Flags"` - item flags such as `"BuyingStore"`, `"DeadBranch"`, `"BindOnEquip"`, etc...\n- `"Delay"` - item use delay\n- `"Stack"` - item stack amount\n- `"NoUse"` - conditions when the item is unusable\n- `"AliasName"` - another item\'s AegisName to be sent to client instead of this AegisName\n\n## Contributing\n\nThis project uses [poetry](https://python-poetry.org/) to manage the development environment.\n\n* Setup a local development environment with `poetry install`\n* Run tests with `poetry run tox` (or `pytest` for current python version)\n* Execute script with `poetry run dp2rathena`\n\n## Changelog\n\nSee [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)\n\n## License\n\nSee [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)\n',
    'author': 'Eric Liu',
    'author_email': 'latiosworks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Latiosu/dp2rathena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

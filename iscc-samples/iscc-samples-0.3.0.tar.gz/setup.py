# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_samples']

package_data = \
{'': ['*'],
 'iscc_samples': ['files/all/*',
                  'files/audio/*',
                  'files/image/*',
                  'files/text/*',
                  'files/video/*']}

setup_kwargs = {
    'name': 'iscc-samples',
    'version': '0.3.0',
    'description': 'A collection of media files as sample data for ISCC testing.',
    'long_description': '# Test data for ISCC\n\n\n## Installation\n\n```console\n$ pip install iscc-samples\n```\n\n## Usage:\n```python\nimport iscc_samples as samples\n\nfor path in samples.videos():\n    print(path)\n```\n\n## Development\n\n### Making a release\n\n```console\n$ poetry build -f sdist\n$ poetry publish\n```\n\n\n## Maintainers\n\n[@titusz](https://github.com/titusz)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nYou may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.\n\n\n## Change Log\n\n### [0.3.0] - 2021-02-17\n- Add powerpoint sample files\n\n### [0.2.0] - 2021-01-25\n\n- Add iscc_samples.all()\n- Return files in sorted order\n\n### [0.1.0] - 2021-01-25\n\n- Initial release with basic sample files\n\n## License\n\nCC-BY-4.0 © 2021 Titusz Pan\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iscc/iscc-samples',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cm-http-api']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.0.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'selenium>=3.141.0,<3.142.0']

setup_kwargs = {
    'name': 'cm-http-api',
    'version': '0.1.0',
    'description': 'get necessary information for Unified certification of educational administration system',
    'long_description': "# A Solution to get timetable automatically\n\nThis is designed at first to get excel timetable from http://my.cqu.edu.cn/enroll/\nbut failed at last because of js Ajax loading of specific page. I tried every method I can but gave up at last.\n</br>\nSo this solution maybe design for getting token for logging in process as we have known that all requests need this\ntoken.\n\n# Usage\n\nRefer to `main` function of [main.py](main.py) as a demo, and docstring of `cm_http` class.\n\n# To List\n\n- [x] get token\n- [x] get json format timetable\n- [ ] parsing timetable.json translate it to `xlsx` format for example\n- [ ] using in [cqu_timetable_new](https://github.com/weearc/cqu_timetable_new)\n\nAlthough I'd like to use these scripts on desktop, more people seem to get an automatically one.\n</br>\nAnother reason why I have to build this is that I hate the new `wecqu` under the `Student Union of CQU`. I'd like to use\nAGPL to force them ether opensource of their code or make another one without my function.\n\n# License\nAGPL 3.0\n",
    'author': 'weearc',
    'author_email': 'qby19981121@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/weearc/cm-http-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.1',
}


setup(**setup_kwargs)

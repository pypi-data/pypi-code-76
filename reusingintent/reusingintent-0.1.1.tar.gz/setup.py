# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reusingintent',
 'reusingintent.inference_core',
 'reusingintent.inference_core.algorithms',
 'reusingintent.inference_core.reapply',
 'reusingintent.inference_core.reapply.data_structures',
 'reusingintent.inference_core.reapply.reapply_algorithms',
 'reusingintent.server',
 'reusingintent.server.celery',
 'reusingintent.server.database',
 'reusingintent.server.database.schemas',
 'reusingintent.server.database.schemas.algorithms',
 'reusingintent.server.routes',
 'reusingintent.server.routes.dataset',
 'reusingintent.server.routes.project',
 'reusingintent.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Cors>=3.0.9,<4.0.0',
 'Flask>=1.1.2,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy>=1.3.20,<2.0.0',
 'celery>=5.0.5,<6.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'paretoset>=1.2.0,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'reusingintent',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Kiran Gadhave',
    'author_email': 'kirangadhave2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

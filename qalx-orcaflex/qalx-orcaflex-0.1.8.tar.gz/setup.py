# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qalx_orcaflex',
 'qalx_orcaflex.bots',
 'qalx_orcaflex.bots.batch',
 'qalx_orcaflex.bots.sim',
 'qalx_orcaflex.core',
 'qalx_orcaflex.data_models',
 'qalx_orcaflex.data_models.notifications',
 'qalx_orcaflex.gui',
 'qalx_orcaflex.gui.batch',
 'qalx_orcaflex.gui.batch.models',
 'qalx_orcaflex.helpers',
 'qalx_orcaflex.video']

package_data = \
{'': ['*'],
 'qalx_orcaflex.data_models.notifications': ['templates/*'],
 'qalx_orcaflex.gui': ['icons/*']}

install_requires = \
['OrcFxAPI>=11.0.2,<12.0.0',
 'PyQt5>=5.15.1,<6.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psutil>=5.7.0,<6.0.0',
 'pyqalx>=0.14.1',
 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{'docs': ['sphinx>=2.1,<3.0', 'sphinx-rtd-theme>=0.4.3,<0.5.0'],
 'pip-licenses': ['pip-licenses>=1.16,<2.0']}

setup_kwargs = {
    'name': 'qalx-orcaflex',
    'version': '0.1.8',
    'description': 'qalx bots and helpers for OrcaFlex',
    'long_description': "# qalx-orcaflex\n\nTools to help you run OrcaFlex on [qalx](https://qalx.net).\n\n> To use this package you'll need a **qalx** API key.\n> This can be obtained by registering at [qalx.net](https://qalx.net#section-contact). \n>\n## Features\n\nThe current features are:\n\n- **Batches**: build batches of OrcaFlex data files from various sources\n- **Results**: attach some required results which will be extracted automatically when the simulation is complete. The results will also be summarised for each batch\n- **Load case information**: results in a batch can be linked to information about the load case\n- **Model views**: define a set of model views that will be automatically captured at the end of the simulation\n- **Smart statics**: allows you to add object tags that will be used to iteratively find a model that solves in statics\n\nSome planned features:\n\n-  Custom results specification\n-  Linked Statistics and Extreme Statistics\n-  Model views at key result points (e.g. max of a time history)\n-  Model video extraction\n-  Optional progress screenshots\n-  Automatic batch cancellation on result breach\n-  Allowed to define “Model deltas” from a base model\n-  Option to extract all model data into qalx (useful if you want to do analytics/ML on model/sim data over time)\n\n## Installation\n\n```bash\npip install qalx-orcaflex\n```\n\n## Documentation\n\n[This can be found here.](https://orcaflex.qalx.net)\n\n## Questions?\n\nPlease [send us an email (info@qalx.net)](mailto:info@qalx.net)! \n",
    'author': 'Steven Rossiter',
    'author_email': 'steve@agiletek.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

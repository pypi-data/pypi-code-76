# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napari_arnheim',
 'napari_arnheim.registries',
 'napari_arnheim.widgets',
 'napari_arnheim.widgets.context',
 'napari_arnheim.widgets.details',
 'napari_arnheim.widgets.dialogs',
 'napari_arnheim.widgets.dialogs.forms',
 'napari_arnheim.widgets.dialogs.forms.fields',
 'napari_arnheim.widgets.dialogs.forms.fields.selectors',
 'napari_arnheim.widgets.dialogs.forms.fields.selectors.models',
 'napari_arnheim.widgets.dialogs.forms.models',
 'napari_arnheim.widgets.error',
 'napari_arnheim.widgets.items',
 'napari_arnheim.widgets.lists',
 'napari_arnheim.widgets.tables']

package_data = \
{'': ['*']}

install_requires = \
['bergen>=0.3.30,<0.4.0',
 'grunnlag>=0.2.9,<0.3.0',
 'napari>=0.4.2,<0.5.0',
 'pyqt5>=5.12.5,<6.0.0',
 'pyqtwebengine>=5.15.2,<6.0.0',
 'qasync>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['napari-arnheim = napari_arnheim.run:main']}

setup_kwargs = {
    'name': 'napari-arnheim',
    'version': '0.1.6',
    'description': 'Napari with Arnheim Client Integrated',
    'long_description': '# Napari - Arnheim\n\n### Idea\n\nNapari Arnheim bundles Napari with the Arnheim Framework Client and its Grunnlag-Provider\n\n \n### Prerequisites\n\nNapari Arnheim only works with a running Arnheim Instance (in your network or locally for debugging) and a Grunnlag-Provider. (see Grunnlag)\n\n### Usage\n\nIn order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance\n\n```python\n\nbergen = Bergen(host="HOST_NAME",\n    port=8000,\n  client_id="APPLICATION_ID_FROM_ARNHEIM", \n  client_secret="APPLICATION_SECRET_FROM_ARNHEIM",\n  name="karl",\n)\n\n\nwith napari.gui_qt():\n    viewer = napari.Viewer()\n    viewer.window.add_dock_widget(ArnheimWidget(bergen=bergen), area="right")\n\n\n```\n\n### Testing and Documentation\n\nSo far Bergen does only provide limitedunit-tests and is in desperate need of documentation,\nplease beware that you are using an Alpha-Version\n\n\n### Build with\n\n- [Arnheim](https://github.com/jhnnsrs/arnheim)\n- [Bergen](https://github.com/jhnnsrs/bergen)\n- [Grunnlag](https://github.com/jhnnsrs/grunnlag)\n- [Napari](https://github.com/napari/napari)\n\n\n\n## Roadmap\n\nThis is considered pre-Alpha so pretty much everything is still on the roadmap\n\n\n## Deployment\n\nContact the Developer before you plan to deploy this App, it is NOT ready for public release\n\n## Versioning\n\nThere is not yet a working versioning profile in place, consider non-stable for every release \n\n## Authors\n\n* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)\n\nSee also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.\n\n## License\n\nAttribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) \n\n## Acknowledgments\n\n* EVERY single open-source project this library used (the list is too extensive so far)',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhnnsrs/napari-arnheim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

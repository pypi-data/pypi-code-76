# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fiji_arnheim', 'fiji_arnheim.macros', 'fiji_arnheim.registries']

package_data = \
{'': ['*']}

install_requires = \
['bergen>=0.3.31,<0.4.0', 'grunnlag>=0.2.9,<0.3.0', 'pyimagej>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['fiji-arnheim = fiji_arnheim.run:main']}

setup_kwargs = {
    'name': 'fiji-arnheim',
    'version': '0.1.3',
    'description': 'Fiji with Arnheim Client Integrated',
    'long_description': '# Fiji - Arnheim\n\n### Disclaimer\n\nThis is alpha software. Versioning is errounous. Breaking changes happening on a daily basis. If you want to test the Arnheim platform please contact the developers directly.\n\n### Idea\n\nFiji-Arnheim provides a simple interface to start Fiji and connect it to a local Arnheim Instance. Fiji register itself\nas a worker and provides implementations to common image analysis tasks. ImageJ-1 Macros are supported to wrap and are registered\nas templates for the Tasks. (For detailed information on how Arnheim thinks about tasks and templates please visit the Arnheim\ndocumentation)\n\n \n### Prerequisites and Install\n\nFiji Arnheim heavily relies on PyImageJ for interfacing with ImageJ/Fiji. PyImageJ itself has various dependencies on Java and Maven.\nYou can install PyImageJ via conda and then install Fiji Arnheim on top.\n\n```\nconda create -n fijiarnheim pyimagej openjdk=8\nconda activate fijiarnheim\npip install fiji-arnheim\n\n```\n\nThis install pyimagej together with maven. PyImageJ is then taking care of setting up a local instance of Fiji.\n\n\n### Usage\n\nIn order to run fiji-arnheim, activate your environment and run\n```\nfiji-arnheim\n```\nThis will open Fiji with its UI (Usage is standard Fiji) and register it as a worker. You can call its implementations\nnow from anywhere\n\n\n### Use Cases\n\nPlease read the Arnheim documentation thoroughly to get an idea for the use-cases and limitations of the Arnheim platform.\nUse cases include:\n\n  1. Remote Image Analysis: Use data stored on your institute server and analyse it on your local machine, without downloading and storing your data.\n  2. Big Data: Stream big datasets to your local machine (Napari required)\n  3. Combined Analysis Flows: Use Deeplearning in the Cloud, Cluster analysis, Web apps and Clients like ImageJ and Napari all in one analysis flow with metadata storage.\n  4. End-to-End Pipelines: Acquire Images on your Microscope, process them on the fly and get notified about results.\n\nPlease contact the developer for better explainations.\n\n\n### Testing and Documentation\n\nSo far Arnheim Fiji does only provide limitedunit-tests and is in desperate need of documentation,\nplease beware that you are using an Alpha-Version\n\n\n### Build with\n\n- [Arnheim](https://github.com/jhnnsrs/arnheim)\n- [Bergen](https://github.com/jhnnsrs/bergen)\n- [Grunnlag](https://github.com/jhnnsrs/grunnlag)\n- [PyImage](https://github.com/imagej/pyimagej)\n\n\n\n## Roadmap\n\nThis is considered pre-Alpha so pretty much everything is still on the roadmap\n\n\n## Deployment\n\nContact the Developer before you plan to deploy this App, it is NOT ready for public release\n\n## Versioning\n\nThere is not yet a working versioning profile in place, consider non-stable for every release \n\n## Authors\n\n* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)\n\nSee also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.\n\n## License\n\nAttribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) \n\n## Acknowledgments\n\n* EVERY single open-source project this library used (the list is too extensive so far)',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhnnsrs/fiji-arnheim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cogment']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-reflection',
 'grpcio==1.30',
 'prometheus-client>=0.8.0,<0.9.0',
 'protobuf>=3.7']

setup_kwargs = {
    'name': 'cogment',
    'version': '1.0.0a7',
    'description': 'Cogment python SDK',
    'long_description': '# cogment python SDK\n\n> ⚠️ 🚧 This is part of an upcoming release of cogment and still unstable.\n>\n> Current stable version can be found at <https://gitlab.com/cogment/cogment>\n\n[![Latest final release](https://img.shields.io/pypi/v/cogment?style=flat-square)](https://pypi.org/project/cogment/) [![Apache 2 License](https://img.shields.io/badge/license-Apache%202-green?style=flat-square)](./LICENSE) [![Changelog](https://img.shields.io/badge/-Changelog%20-blueviolet?style=flat-square)](./CHANGELOG.md)\n\n## Introduction\n\nThe Cogment framework is a high-efficiency, open source framework designed to enable the training of models in environments where humans and agents interact with the environment and each other continuously. It’s capable of distributed, multi-agent, multi-model training.\n\nThis is the python API for making use of the cogment framework when working with the Python programming language.\n\nFor further Cogment information, check out the documentation at <https://docs.cogment.ai>\n\n## Developers\n\n### Local setup\n\nMake sure you have the following installed:\n  - [Python](https://www.python.org) (any version >=3.7 should work),\n  - [Poetry](https://python-poetry.org).\n\nInstall the dependencies, including downloading and building the cogment protobuf API, by navigating to the python SDK directory and run the following\n\n```\npoetry install\n```\n\n### Define used Cogment protobuf API\n\nThe version of the used cogment protobuf API is defined in the `.cogment-api.yaml` file at the root of the repository. The following can be defined:\n\n- `cogment_api_version: "latest"`, is the default, it retrieves the _latest_ build of the cogment-api `develop`,\n- `cogment_api_version: "vMAJOR.MINOR.PATCH[-PRERELEASE]"`, retrieves an official release of cogment-api.\n- `cogment_api_path: "../path/to/cogment-api"`, retrieves a local version of cogment-api found at the given path ; if set, this overrides `cogment_api_version`.\n\n> ⚠️ when building a docker image, `cogment_api_path` needs to exists in the docker file system. In practice it means it should be a subdirectory of the current directory.\n\n### Tests\n\nTo run them the first step is to configure the way to launch the orchestrator and the cli in a `.env` file. \n\nYou can copy `.env.template` for an example of what\'s expected.\n\n#### Module tests\n\nThese tests only rely on the sdk, no connection to an orchestrator is done.\n\nTo execute the module tests, simply run\n\n```\npoetry run task test\n```\n\n#### Integration tests\n\nThese tests launch and use an orchestrator they are slower but more in depth. \n\nThen, to execute the integration tests (as well as the module tests), simply run\n\n```\npoetry run task test --launch-orchestrator\n```\n\nThese tests can also be launched in a docker image.\n\n```\ndocker build \\\n  -t cogment/cogment-py-sdk-integration-test:latest \\\n  --build-arg COGMENT_IMAGE="<PATH_TO_COGMENT_IMAGE" \\\n  --build-arg COGMENT_ORCHESTRATOR_IMAGE="<PATH_TO_COGMENT_ORCHESTRATOR_IMAGE" \\\n  -f integration_test.dockerfile .\ndocker run --rm cogment/cogment-py-sdk-integration-test:latest\n```\n\n### Lint\n\nRun the linter using\n\n```\npoetry run task lint\n```\n\n### Build the source package\n\nBuild the source package (this step will only be succesfull if `poetry install` succeeded)\n\n```\npoetry build -f sdist\n```\n\n### Build a Docker image\n\nNavigate to the python SDK directory and run the following in order to create an image that can be used by a cogment project:\n\n```\ndocker build -t image_name .\n```\n\n\n',
    'author': 'Artificial Intelligence Redefined',
    'author_email': 'dev+cogment@ai-r.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cogment.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

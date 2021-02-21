# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['payler']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'aio-pika>=6.7.1,<7.0.0',
 'click>=7.1.2,<8.0.0',
 'motor>=2.3.1,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'prometheus-client>=0.9.0,<0.10.0',
 'pymongo>=3.11.3,<4.0.0']

entry_points = \
{'console_scripts': ['payler = payler.client:run_payler']}

setup_kwargs = {
    'name': 'payler',
    'version': '0.2.0',
    'description': 'Move messages from one source to another one.',
    'long_description': '# Payl[oad Spoo]ler\n\n[![Build Status](https://github.com/tbobm/payler/workflows/payler/badge.svg)](https://github.com/tbobm/payler/workflows/payler/)\n\n\n_Send your payload now, treat it later._\n\n## What is this?\n\nPayler is an asyncio-based Python application intended to provide a way of delaying message execution. The goal of this program is to reduce the workload on your existing message broker solution (Only RabbitMQ is currently supported, but other message-brokers can be easily implemented) by putting the payloads in a storage backend which will then be polled to re-inject payloads in the corresponding destination.\n\n## Installation\n\nThrough pypi:\n```console\n$ pip install payler\n```\n\nThrough [poetry](https://github.com/python-poetry/poetry):\n```console\n$ git clone https://github.com/tbobm/payler\n$ cd payler\n$ poetry install\n```\n\n## How to use this\n\nUsing the command line:\n\n1. Specify the input and output URLs for your drivers (see [configuration](#configuration))\n2. (optional) Customize the configuration to suit your needs _currently the example configuration is the only valid one_\n3. Run payler `payler --config-file configuration.yaml`\n\nUsing the docker image:\n\n1. Pull the docker image `docker pull ghcr.io/tbobm/payler:latest`\n2. (optional) Customize the configuration to suit your needs _currently the example configuration is the only valid one_ (mount the configuration file into the volume at `/configuration.yaml`)\n3. Run the docker image and provide environment variables `docker run -d --name payler -e BROKER_URL="amqp://payler:secret@my-broker/" -e MONGODB_URL="mongodb://payler:secret@my-mongo/payler" ghcr.io/tbobm/payler`\n\n## Configuration\n\nIn order to configure the different workflows, payler uses a configuration file (see [configuration.yml](./configuration.yml)).\n\nExample config file:\n\n```yaml\n---\nworkflows:\n  - name: "Fetch payloads from RabbitMQ and store them in MongoDB"\n    location: "payler"\n    callable: "client.process_queue"\n  - name: "Re-injects payloads to RabbitMQ"\n    callable: "client.watch_storage"\n```\n\nThe `workflows[].name` attribute is currently unused, but will offer a more human-friendly way of getting informed about a workflow\'s state.\nThe `workflows[].location` corresponds to the package where the `workflows[].callable` can be found. It defaults to `payler`, but can this is a way of offering a dumb and simple plugin mechanism by creating function matching the following signature:\n\n```python\nasync def my_workflow(loop: asyncio.AbstractEventLoop) -> None:\n    """My user-defined workflow."""\n    # configure your driver(s)\n    input_driver.serve()\n```\n\n## Features\n\n- Listen to a Broker Queue\n- Store messages with a duration or date as metadata\n- Re-inject the messages after the duration in the default Exchange\n- Output failed messages to global output\n\n## Testing\n\nThis project has unittests with [pytest](https://docs.pytest.org/en/latest/). A wrapper script is available at [run-tests.sh](./run-tests.sh).\n\n## Contributing\n\nFeel free to open new issues for feature requests and bug reports in the [issue page](github.com/tbobm/payler/issues/new) and even create PRs if you feel like it.\n\nThis project is linted with `pylint` with some minor adjustments (see the [setup.cfg](./setup.cfg)).\n\n## Note\n\nThis side-project is born from the following:\n- I wanted to experiment with Python\'s `asyncio`\n- A friend of mine had issues with delaying lots of messages using RabbitMQ\'s [delayed exchange plugin](https://github.com/rabbitmq/rabbitmq-delayed-message-exchange)\n- I was looking for a concrete use-case to work with Github Actions.\n',
    'author': 'Theo "Bob" Massard',
    'author_email': 'tbobm@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tbobm.github.io/payler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

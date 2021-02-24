# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datastreamservicelib']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'datastreamcorelib>=1.1,<2.0',
 'pyzmq>=19.0,<20.0',
 'toml>=0.10,<0.11',
 'tomlkit>=0.6,<0.7']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['testpublisher = '
                     'datastreamservicelib.console:publisher_cli',
                     'testsubscriber = '
                     'datastreamservicelib.console:subscriber_cli']}

setup_kwargs = {
    'name': 'datastreamservicelib',
    'version': '1.9.1',
    'description': '',
    'long_description': '====================\ndatastreamservicelib\n====================\n\nAsyncIO eventloop helpers and Abstract Base Classes for making services that use ZMQ nice, easy and DRY\n\nUsage\n-----\n\nUse the CookieCutter template at https://gitlab.com/advian-oss/python-datastreamserviceapp_template\n\nYou can also take a look at src/datastreamservicelib/console.py for some very simple test examples.\n\nDocker\n------\n\nFor more controlled deployments and to get rid of "works on my computer" -syndrome, we always\nmake sure our software works under docker.\n\nIt\'s also a quick way to get started with a standard development environment.\n\nSSH agent forwarding\n^^^^^^^^^^^^^^^^^^^^\n\nWe need buildkit_::\n\n    export DOCKER_BUILDKIT=1\n\n.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/\n\nAnd also the exact way for forwarding agent to running instance is different on OSX::\n\n    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"\n\nand Linux::\n\n    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"\n\nCreating a development container\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nBuild image, create container and start it (switch the 58449 port to the port from src/datastreamservicelib/defaultconfig.py)::\n\n    docker build --ssh default --target devel_shell -t datastreamservicelib:devel_shell .\n    docker create --name datastreamservicelib_devel -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` datastreamservicelib:devel_shell\n    docker start -i datastreamservicelib_devel\n\npre-commit considerations\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf working in Docker instead of native env you need to run the pre-commit checks in docker too::\n\n    docker exec -i datastreamservicelib_devel /bin/bash -c "pre-commit install"\n    docker exec -i datastreamservicelib_devel /bin/bash -c "pre-commit run --all-files"\n\nYou need to have the container running, see above. Or alternatively use the docker run syntax but using\nthe running container is faster::\n\n    docker run -it --rm -v `pwd`":/app" datastreamservicelib:devel_shell -c "pre-commit run --all-files"\n\nTest suite\n^^^^^^^^^^\n\nYou can use the devel shell to run py.test when doing development, for CI use\nthe "tox" target in the Dockerfile::\n\n    docker build --ssh default --target tox -t datastreamservicelib:tox .\n    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` datastreamservicelib:tox\n\nProduction docker\n^^^^^^^^^^^^^^^^^\n\nThere\'s a "production" target as well for quick running of testsubscriber and testpublisher\n\n    docker build --ssh default --target production -t datastreamservicelib:latest .\n    docker run --rm -it -v /tmp:/tmp datastreamservicelib:latest testpublisher -s ipc:///tmp/test_pub.sock -t foo\n    docker run --rm -it -v /tmp:/tmp datastreamservicelib:latest testsubscriber -s ipc:///tmp/test_pub.sock -t foo\n\nNote that on non-linux platforms the IPC sockets may not as expected between host and container over volume mounts.\n\n\nLocal Development\n-----------------\n\nTLDR:\n\n- Create and activate a Python 3.6 virtualenv (assuming virtualenvwrapper)::\n\n    mkvirtualenv -p `which python3.6` my_virtualenv\n\n- change to a branch::\n\n    git checkout -b my_branch\n\n- install Poetry: https://python-poetry.org/docs/#installation\n- Install project deps and pre-commit hooks::\n\n    poetry install\n    pre-commit install\n    pre-commit run --all-files\n\n- Ready to go, try the following::\n\n    testpublisher --help\n    testsubscriber --help\n\nUse Python 3.6 for development since it\'s the lowest supported version so you don\'t accidentally\nuse features only available in higher versions and then have to re-do everything when CI tests fail\non 3.6.\n\nRemember to activate your virtualenv whenever working on the repo, this is needed\nbecause pylint and mypy pre-commit hooks use the "system" python for now (because reasons).\n\nRunning "pre-commit run --all-files" and "py.test -v" regularly during development and\nespecially before committing will save you some headache.\n',
    'author': 'Eero af Heurlin',
    'author_email': 'eero.afheurlin@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/advian-oss/python-datastreamservicelib/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cci_cli', 'cci_cli.circle', 'cci_cli.commands', 'cci_cli.common']

package_data = \
{'': ['*']}

install_requires = \
['confuse>=1.3,<2.0',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.24,<3.0',
 'tabulate>=0.8,<0.9',
 'timeago>=1.0,<2.0',
 'typer>=0.3,<0.4']

entry_points = \
{'console_scripts': ['cci = cci_cli.main:app']}

setup_kwargs = {
    'name': 'cci-cli',
    'version': '0.1.2',
    'description': 'This is a small CircleCI CLI that allows you to interact with the CircleCI API v2',
    'long_description': '# CircleCI CLI\n\n[![CircleCI](https://circleci.com/gh/lightspeed-hospitality/circleci-cli.svg?style=svg&circle-token=639e11bbab82eb96b4cc285724c17de30fecf8ce)](https://app.circleci.com/pipelines/github/lightspeed-hospitality/circleci-cli)\n\n<p align="center">\n  <a href="#install">Install</a> •\n  <a href="#commands">Commands</a> •\n  <a href="#development">Development</a> •\n  <a href="#how-to-contribute">Contribute</a> •\n  <a href="#support--feedback">Support</a>\n</p>\n\n🛠 WIP\nThis is a small CircleCI CLI that allows you to interact with the [CircleCI API v2](https://circleci.com/docs/api/v2/).\n\n---\n\n## Install\n\n1. If you\'re on macOS, it\'s recommended you install Python 3 via Homebrew first:\n    ```sh\n    brew install python3\n    ```\n\n2. Install `cci`:\n    ```sh\n    pip3 install --user cci-cli\n    ```\n\n3. Open a new shell and type `cci --help`. You should see help output.\n\n    > ⚠️ No output? You might need to update your `PATH`. On macOS, try adding this to your `.zshrc`:\n    > ```sh\n    > export PATH="$PATH:$HOME/Library/Python/3.9/bin"\n    > ```\n    > (check which version of Python 3 you are using).\n\n4. Generate a personal CircleCI API token [here](https://app.circleci.com/settings/user/tokens).\n\n5. Give this token to `cci`:\n    ```sh\n    cci config setup --vcs gh --org lightspeed-hospitality --token <circle-ci-api-token>\n    ```\n\n### Install completions\n\nFor shell completion, run `cci --install-completion zsh` (or `bash`, if you use bash).\n\n> ⚠️ If you use `zsh`, the configuration added to the bottom of your `.zshrc` [is wrong](https://github.com/tiangolo/typer/pull/237) and need to be adjusted. Replace:\n> ```sh\n> compinit\n> zstyle \':completion:*\' menu select\n> fpath+=~/.zfunc\n> ```\n> With:\n> ```sh\n> fpath+=~/.zfunc\n> compinit\n> ```\n\n### Docker\n\nIf you don\'t want to install `cci` locally, you can run it from Docker:\n\n```sh\nalias cci=\'docker pull lightspeedhq-ls-container-dev.jfrog.io/circleci-cli && docker run -it --rm --volume=$HOME/.config/circleci-cli:/root/.config/circleci-cli lightspeedhq-ls-container-dev.jfrog.io/circleci-cli\'\n```\n\n## Commands\n\n**Display your config**\n```\ncci config show\n```\n\n\n**List the last 20 pipelines for `<project-name>`**\n```\ncci pipelines list <project-name>\n```\n\n**Trigger a build for `<project-name>` using `<branch>`**\n```\ncci pipelines trigger <project-name> --branch <branch> [--wait-for-result] [--timeout <min>] [--params key=value,...]\n```\n\n## Development\n\n### Setup\n\nFor development, best create a virtual environment and install all dependencies:\n```console\npython3 -m venv venv\n. venv/bin/activate\npip install -r requirements.txt\n```\n\n### Build\n\nYou can create a docker image on your local machine by:\n```console\ndocker build . -t circleci-cli\n```\n\n### Run\n\nIn order to run the build you created on your local machine, run:\n```console\ndocker run -it --rm --volume=$HOME/.config/circleci-cli:/root/.config/circleci-cli circleci-cli\n```\n\n## How to Contribute\n\nIn order to contribute you just have to have Python installed on your machine. In case you do not have it installed get it from [python.org](https://www.python.org/downloads/).\n\n#### Linting Tool\n\nThis project is using [pre-commit](https://pre-commit.com/) to enable linting and auto-formatting as a pre-commit hook.\nThe hooks are configured in [.pre-commit-config.yaml](./.pre-commit-config.yaml).\n\nTo install the hooks you have to run the following command (only once):\n```bash\n. venv/bin/activate\npre-commit install\n```\n\nThen you can trigger all the hooks manually by running:\n```bash\n. venv/bin/activate\npre-commit run --all-files\n```\n\nAdditionally on every `git commit` the hooks will be triggered and have to pass.\n\n#### How to run tests\n\nYou can run all the tests, by simply running:\n```bash\n. venv/bin/activate\npython -m pytest\n```\n\n## Support & Feedback\n\nYour contribution is very much appreciated. Feel free to create a PR or an Issue with your suggestions for improvements.\n',
    'author': 'Lightspeed Hospitality',
    'author_email': 'pt.hospitality.dev@lightspeedhq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

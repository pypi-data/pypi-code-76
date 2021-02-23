# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openconnect_sso', 'openconnect_sso.browser']

package_data = \
{'': ['*']}

install_requires = \
['PySocks>=1.7.1,<2.0.0',
 'attrs>=18.2',
 'colorama>=0.4,<0.5',
 'keyring>=21.1,<23.0.0',
 'lxml>=4.3,<5.0',
 'prompt-toolkit>=3.0.3,<4.0.0',
 'pyxdg>=0.26,<0.27',
 'requests>=2.22,<3.0',
 'setuptools>40.0',
 'structlog>=20.1,<21.2.0',
 'toml>=0.10,<0.11']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.4.0,<2.0.0'],
 'full': ['PyQt5>=5.12,<6.0', 'PyQtWebEngine>=5.12,<6.0']}

entry_points = \
{'console_scripts': ['openconnect-sso = openconnect_sso.cli:main']}

setup_kwargs = {
    'name': 'openconnect-sso',
    'version': '0.6.3',
    'description': 'Wrapper script for OpenConnect supporting Azure AD (SAMLv2) authentication to Cisco SSL-VPNs',
    'long_description': '# openconnect-sso\n\nWrapper script for OpenConnect supporting Azure AD (SAMLv2) authentication\nto Cisco SSL-VPNs\n\n[![Tests Status\n](https://github.com/vlaci/openconnect-sso/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/vlaci/openconnect-sso/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n\n## Installation\n\n### Using pip/pipx\n\nA generic way that works on most \'standard\' Linux distributions out of the box.\nThe following example shows how to install `openconect-sso` along with its\ndependencies including Qt:\n\n```shell\n$ pip install --user pipx\nSuccessfully installed pipx\n$ pipx install "openconnect-sso[full]"\n⣾ installing openconnect-sso\n  installed package openconnect-sso 0.4.0, Python 3.7.5\n  These apps are now globally available\n    - openconnect-sso\n⚠️  Note: \'/home/vlaci/.local/bin\' is not on your PATH environment variable.\nThese apps will not be globally accessible until your PATH is updated. Run\n`pipx ensurepath` to automatically add it, or manually modify your PATH in your\nshell\'s config file (i.e. ~/.bashrc).\ndone! ✨ 🌟 ✨\nSuccessfully installed openconnect-sso\n$ pipx ensurepath\nSuccess! Added /home/vlaci/.local/bin to the PATH environment variable.\nConsider adding shell completions for pipx. Run \'pipx completions\' for\ninstructions.\n\nYou likely need to open a new terminal or re-login for the changes to take\neffect. ✨ 🌟 ✨\n```\n\nIf you have Qt 5.x installed, you can skip the installation of bundled Qt version:\n\n``` bash\npipx install openconnect-sso\n```\n\nOf course you can also install via `pip` instead of `pipx` if you\'d like to\ninstall system-wide or a virtualenv of your choice.\n\n### On Arch Linux\n\nThere is an unofficial package available for Arch Linux on\n[AUR](https://aur.archlinux.org/packages/openconnect-sso/). You can use your\nfavorite AUR helper to install it:\n\n``` shell\nyay -S openconnect-sso\n```\n\n### Using nix\n\nThe easiest method to try is by installing directly:\n\n```shell\n$ nix-env -i -f https://github.com/vlaci/openconnect-sso/archive/master.tar.gz\nunpacking \'https://github.com/vlaci/openconnect-sso/archive/master.tar.gz\'...\n[...]\ninstalling \'openconnect-sso-0.4.0\'\nthese derivations will be built:\n  /nix/store/2z47740z1rr2cfqfin5lnq04sq3c5xjg-openconnect-sso-0.4.0.drv\n[...]\nbuilding \'/nix/store/50q496iqf840wi8b95cfmgn07k6y5b59-user-environment.drv\'...\ncreated 606 symlinks in user environment\n$ openconnect-sso\n```\n\nAn overlay is also available to use in nix expressions:\n\n``` nix\nlet\n  openconnectOverlay = import "${builtins.fetchTarball https://github.com/vlaci/openconnect-sso/archive/master.tar.gz}/overlay.nix";\n  pkgs = import <nixpkgs> { overlays = [ openconnectOverlay ]; };\nin\n  #  pkgs.openconnect-sso is available in this context\n```\n\n... or to use in `configuration.nix`:\n\n``` nix\n{ config, ... }:\n\n{\n  nixpkgs.overlays = [\n    (import "${builtins.fetchTarball https://github.com/vlaci/openconnect-sso/archive/master.tar.gz}/overlay.nix")\n  ];\n}\n```\n\n### Windows *(EXPERIMENTAL)*\n\nInstall with [pip/pipx](#using-pippipx) and be sure that you have `sudo` and `openconnect`\nexecutable commands in your PATH.\n\n## Usage\n\nIf you want to save credentials and get them automatically\ninjected in the web browser:\n\n```shell\n$ openconnect-sso --server vpn.server.com/group --user user@domain.com\nPassword (user@domain.com):\n[info     ] Authenticating to VPN endpoint ...\n```\n\nUser credentials are automatically saved to the users login keyring (if\navailable).\n\nIf you already have Cisco AnyConnect set-up, then `--server` argument is\noptional. Also, the last used `--server` address is saved between sessions so\nthere is no need to always type in the same arguments:\n\n```shell\n$ openconnect-sso\n[info     ] Authenticating to VPN endpoint ...\n```\n\nConfiguration is saved in `$XDG_CONFIG_HOME/openconnect-sso/config.toml`. On\ntypical Linux installations it is located under\n`$HOME/.config/openconnect-sso/config.toml`\n\n## Development\n\n`openconnect-sso` is developed using [Nix](https://nixos.org/nix/). Refer to the\n[Quick Start section of the Nix\nmanual](https://nixos.org/nix/manual/#chap-quick-start) to see how to get it\ninstalled on your machine.\n\nTo get dropped into a development environment, just type `nix-shell`:\n\n```shell\n$ nix-shell\nSourcing python-catch-conflicts-hook.sh\nSourcing python-remove-bin-bytecode-hook.sh\nSourcing pip-build-hook\nUsing pipBuildPhase\nSourcing pip-install-hook\nUsing pipInstallPhase\nSourcing python-imports-check-hook.sh\nUsing pythonImportsCheckPhase\nRun \'make help\' for available commands\n\n[nix-shell]$\n```\n\nTo try an installed version of the package, issue `nix-build`:\n\n```shell\n$ nix build\n[1 built, 0.0 MiB DL]\n\n$ result/bin/openconnect-sso --help\n```\n\nAlternatively you may just [get Poetry](https://python-poetry.org/docs/) and\nstart developing by using the included `Makefile`. Type `make help` to see the\npossible make targets.\n',
    'author': 'László Vaskó',
    'author_email': 'laszlo.vasko@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vlaci/openconnect-sso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

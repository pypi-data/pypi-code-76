# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amdfan']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.20.1,<2.0.0',
 'rich>=9.10.0,<10.0.0']

entry_points = \
{'console_scripts': ['amdfan = amdfan.amdfan:cli']}

setup_kwargs = {
    'name': 'amdfan',
    'version': '0.1.6',
    'description': 'Fan monitor and controller for AMD gpus in Linux',
    'long_description': '# AmdFan\n![Python package](https://github.com/mcgillij/amdfan/workflows/Python%20package/badge.svg)\n\nIs a fork of amdgpu-fan, with security updates and added functionality.\n\n## Why fork?\n\n* alternatives abandoned\n* lacking required features\n* security fixes not addressed\n* basic functionality not working \n\n### Amdgpu_fan abandoned\n\nAs of a couple years ago, and isn’t applying any security fixes to their project or improvements. There were also some bugs that bothered me with the project when I tried to get it up and running.\nFeatures missing\n\nThere are a number of features that I wanted, but weren’t available.\n\n* Thresholds allow temperature range before changing fan speed\n* Frequency setting to allow better control\n* Monitoring to be able to see real-time fan speeds and temperature \n\n### Security Fixes\n\nThere are some un-addressed pull requests for some recent YAML vulnerabilities that are still present in the old amdgpu_fan project, that I’ve addressed in this fork.\n\n### Basic functionality\n\nSetting the card to system managed using the amdgpu_fan pegs your GPU fan at 100%, instead of allowing the system to manage the fan settings. I fixed that bug as well in this release.\n\nThese are all addressed in Amdfan, and as long as I’ve still got some AMD cards I intend to at least maintain this for myself. And anyone’s able to help out since this is open source. I would have liked to just contribute these fixes to the main project, but it’s now inactive.\n\n# Documentation\n## Usage\n\n``` bash\nUsage: amdfan.py [OPTIONS]\n\nOptions:\n  --daemon         Run as daemon applying the fan curve\n  --monitor        Run as a monitor showing temp and fan speed\n  --manual         Manually set the fan speed value of a card\n  --configuration  Prints out the default configuration for you to use\n  --service        Prints out the amdfan.service file to use with systemd\n  --help           Show this message and exit.\n```\n\n## Daemon\n\nAmdfan is also runnable as a systemd service, with the provided ```amdfan.service```.\n\n## Monitor\n\nYou can use Amdfan to monitor your AMD video cards using the ```--monitor``` flag.\n\n![screenshot](https://raw.githubusercontent.com/mcgillij/amdfan/main/images/screenshot.png)\n\n## Manual\n\nAlternatively if you don\'t want to set a fan curve, you can just apply a fan setting manually. \nAlso allows you to revert the fan control to the systems default behavior by using the "auto" parameter.\n![screenshot](https://raw.githubusercontent.com/mcgillij/amdfan/main/images/manual.png)\n\n## Configuration\n\nThis will dump out the default configuration that would get generated for `/etc/amdfan.yml` when you first run it as a service. This allows you to configure the settings prior to running it as a daemon if you wish.\n\n## Service\n\nThis is just a convenience method for dumping out the `amdfan.service` that would get installed if you used a package manager to install amdfan. Useful if you installed the module via `pip`, `pipenv` or `poetry` vs using the package manager version.\n\n\n\n## Note\n\nYou will need to ```sudo``` to apply any changes to the fan speeds, but you can monitor them with regular user permissions.\n\n# Config File example\n\n``` yaml\n# [<Temp in C>,<Fanspeed in %>]\nspeed_matrix:\n- [4, 4]\n- [30, 33]\n- [45, 50]\n- [60, 66]\n- [65, 69]\n- [70, 75]\n- [75, 89]\n- [80, 100]\n\n# Current Min supported value is 4 due to driver bug\n#\n# Optional configuration options\n#\n# Allows for some leeway +/- temp, as to not constantly change fan speed\n# threshold: 2\n#\n# Frequency will chance how often we probe for the temp\n# frequency: 5\n#\n# cards:\n# can be any card returned from `ls /sys/class/drm | grep "^card[[:digit:]]$"`\n# - card0\n```\n\n## Running the systemd service\n\nTo run the service, if you installed amdfan using the AUR package, you can run the following commands to **start/enable** the service.\n\n``` bash\nsudo systemctl start amdfan\nsudo systemctl enable amdfan\n```\n\nAfter you\'ve started it, you may want to edit the settings found in `/etc/amdfan.yml`. Once your happy with those, you can restart amdfan with the following command.\n\n``` bash\nsudo systemctl restart amdfan\n```\n\n## Checking the status\nYou can check the systemd service status with the following command:\n\n``` bash\nsystemctl status amdfan\n```\n\n## Building Python package\nRequires Poetry to be installed\n\n``` bash \npoetry build\n```\n\n## Building Arch package\n\nBuilding the Arch package assumes you already have a chroot env setup to build packages.\n\n```bash\npoetry build\nmakechrootpkg -c -r $HOME/$CHROOT\n```\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mcgillij.dev/pages/amdfan.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

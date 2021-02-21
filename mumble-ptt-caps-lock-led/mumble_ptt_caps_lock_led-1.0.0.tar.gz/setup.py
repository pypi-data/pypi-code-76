# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mumble_ptt_caps_lock_led']

package_data = \
{'': ['*']}

install_requires = \
['pydbus>=0.6.0,<0.7.0', 'pygobject>=3.38.0,<4.0.0']

entry_points = \
{'console_scripts': ['mpcll_read_ptt_state = '
                     'mumble_ptt_caps_lock_led.read_ptt_state:main',
                     'mpcll_set_caps_led_from_pipe = '
                     'mumble_ptt_caps_lock_led.set_caps_led_from_pipe:main']}

setup_kwargs = {
    'name': 'mumble-ptt-caps-lock-led',
    'version': '1.0.0',
    'description': 'A python program to let the LED of your caps lock key display your mumble PTT state.',
    'long_description': '# mumble_ptt_caps_lock_led\nA python program to let the LED of your caps lock key display your mumble PTT state.\n\nThis is very nice if caps lock is also the PTT key.\nTo do that first disable the caos lock key: `setxkbmap -option ctrl:nocaps`\n\nThis program is split into two parts:\n  - Script to update the LED using `/sys/`. This needs to be run as root.\n  - Script to extract the PTT state from mumble.\n\nThe second script uses the dbus messages of mumble updating the taskbar icon.\nFor this to work, the taskbar icon needs to be enabled.\n',
    'author': 'Tim Neumann',
    'author_email': 'neumantm@fius.informatik.uni-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neumantm/mumble_ptt_caps_lock_led',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

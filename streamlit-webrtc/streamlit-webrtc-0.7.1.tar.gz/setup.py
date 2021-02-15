# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_webrtc']

package_data = \
{'': ['*']}

install_requires = \
['aiortc>=1.1.2,<2.0.0', 'streamlit>=0.73.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'streamlit-webrtc',
    'version': '0.7.1',
    'description': '',
    'long_description': '# streamlit-webrtc\n\n[![Tests](https://github.com/whitphx/streamlit-webrtc/workflows/Tests/badge.svg?branch=master)](https://github.com/whitphx/streamlit-webrtc/actions?query=workflow%3ATests+branch%3Amaster)\n[![Frontend Tests](https://github.com/whitphx/streamlit-webrtc/workflows/Frontend%20tests/badge.svg?branch=master)](https://github.com/whitphx/streamlit-webrtc/actions?query=workflow%3A%22Frontend+tests%22+branch%3Amaster)\n\n[![PyPI](https://img.shields.io/pypi/v/streamlit-webrtc)](https://pypi.org/project/streamlit-webrtc/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/streamlit-webrtc)](https://pypi.org/project/streamlit-webrtc/)\n[![PyPI - License](https://img.shields.io/pypi/l/streamlit-webrtc)](https://pypi.org/project/streamlit-webrtc/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-webrtc)](https://pypi.org/project/streamlit-webrtc/)\n\n[![GitHub Sponsors](https://img.shields.io/github/sponsors/whitphx?label=Sponsor%20me%20on%20GitHub%20Sponsors&style=social)](https://github.com/sponsors/whitphx)\n\n<a href="https://www.buymeacoffee.com/whitphx" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180" height="50" ></a>\n\n## Example [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/whitphx/streamlit-webrtc-example/main/app.py)\nYou can try out the sample app using the following commands.\n```\n$ pip install streamlit-webrtc opencv-python\n$ streamlit run https://raw.githubusercontent.com/whitphx/streamlit-webrtc-example/main/app.py\n```\n\nYou can also try it out on [Streamlit Sharing](https://share.streamlit.io/whitphx/streamlit-webrtc-example/main/app.py).\n\nThe deployment of this sample app is managed in this repository: https://github.com/whitphx/streamlit-webrtc-example/.\n\n## Tutorial\n[This post](https://dev.to/whitphx/build-a-web-based-real-time-computer-vision-app-with-streamlit-57l2) explains how to use `streamlit-webrtc` to build a real-time computer vision app.\n',
    'author': 'Yuichiro Tsuchiya',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whitphx/streamlit-webrtc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

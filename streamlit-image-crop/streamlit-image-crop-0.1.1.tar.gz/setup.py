# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_image_crop']

package_data = \
{'': ['*'],
 'streamlit_image_crop': ['frontend/.prettierrc',
                          'frontend/build/*',
                          'frontend/build/static/css/*',
                          'frontend/build/static/js/*']}

install_requires = \
['streamlit>=0.76.0,<0.77.0']

setup_kwargs = {
    'name': 'streamlit-image-crop',
    'version': '0.1.1',
    'description': 'A Streamlit component based on React Image Crop.',
    'long_description': '# Streamlit Image Crop\n\nA [Streamlit](https://www.streamlit.io/) component based on [React Image Crop](https://github.com/DominicTobias/react-image-crop).\n\n![Screenshot](https://raw.githubusercontent.com/mitsuse/streamlit-image-crop/master/screenshot.png)\n\n## Installation\n\n```\npip install streamlit-image-crop\n```\n\n## Example\n\nTry [example.py](https://github.com/mitsuse/streamlit-image-crop/blob/master/example.py).\n\nFirst, you need to install dependencies:\n\n```\ngit clone https://github.com/mitsuse/streamlit-image-crop.git && cd streamlit-image-crop\npip install poetry\npoetry install\n```\n\nNext, run `react-script start`:\n\n```\ncd streamlit-image-crop/frontend/ && npm run start\n```\n\nFinally, run the example:\n\n```\npoetry run streamlit run example.py\n```\n\n## License\n\nStreamlit Image Crop is licensed under the ISC license.\nPlease read [LICENSE](https://github.com/mitsuse/streamlit-image-crop/blob/master/LICENSE) for the detail.\n',
    'author': 'Tomoya Kose',
    'author_email': 'tomoya@mitsuse.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mitsuse/streamlit-image-crop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

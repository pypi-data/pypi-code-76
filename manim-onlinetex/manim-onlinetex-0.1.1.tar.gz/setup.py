# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_onlinetex']

package_data = \
{'': ['*']}

install_requires = \
['manim', 'requests']

entry_points = \
{'manim.plugins': ['manim_onlinetex = manim_onlinetex']}

setup_kwargs = {
    'name': 'manim-onlinetex',
    'version': '0.1.1',
    'description': 'A Manim Plugin that renders LaTeX for Mobjects like Tex and MathTex via online services.',
    'long_description': "# manim-onlinetex\n\nA Manim Plugin that renders LaTeX for Mobjects like `Tex` and `MathTex` via online services.\nThis plugin will try to render the LaTeX required by such Mobjects via [LatexCluster](https://latexcluster.org/), and if for some reason LatexCluster is down, will attempt to use [QuickLaTeX](https://quicklatex.com/).\n\n## Usage instructions\n\nImport the contents of `manim_onlinetex` AFTER `manim` has been imported, like so:\n\n```py\nfrom manim import *\nfrom manim_onlinetex import *\n```\n\nThen, use a `Mobject` that requires `LaTeX` rendering. If the\nPlugin is doing its job, then the `Tex` folder of your `media`\ndirectory should have the source `.tex` file, the final `.svg` \nfile, and no intermediary files (like `.dvi` files), since that's\nall handled by the online service.\n\n## Limitations\n\nPlease avoid clearing the Tex directory of your media directory. This is so you don't contact the external LaTeX rendering APIs too often and put an unnecessary strain on their servers.\n",
    'author': 'The Manim Community Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

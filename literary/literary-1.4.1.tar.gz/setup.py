# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['literary', 'literary.commands', 'literary.notebook']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'ipython>=7.19.0,<8.0.0',
 'nbclient>=0.5.1,<0.6.0',
 'nbconvert>=6.0.7,<7.0.0',
 'nbformat[fast]>=5.0.8,<6.0.0',
 'toml>=0.10.2,<0.11.0',
 'traitlets>=5.0.5,<6.0.0']

extras_require = \
{':python_version < "3.9"': ['astunparse>=1.6.3,<2.0.0']}

entry_points = \
{'console_scripts': ['literary = literary.__main__:run']}

setup_kwargs = {
    'name': 'literary',
    'version': '1.4.1',
    'description': 'Literate package development with Jupyter',
    'long_description': '![Literary logo with an orange cursive uppercase L inside black square brackets](assets/logo.png)\n\n# Literary \n[![pypi-badge][]][pypi] [![binder-badge][]][binder]  \n\n[binder]:\n  https://mybinder.org/v2/gh/agoose77/literary/HEAD?urlpath=lab%2Ftree%2Fexamples\n[binder-badge]: https://mybinder.org/badge_logo.svg\n[pypi-badge]: https://img.shields.io/pypi/v/literary\n[pypi]: https://pypi.org/project/literary\n\nThis package is an exploration of the [literate programming](http://www.literateprogramming.com) idea [pioneered by\n Donald\nKnuth](https://www-cs-faculty.stanford.edu/~knuth/lp.html) and implemented in the\n [`nbdev` package](https://github.com/fastai/nbdev). Although `nbdev` looks to be a very\nmature and comprehensive tool, it is quite opinionated. This package is an\ninvestigation into what a smaller `nbdev` might look like.\n\n## Philosophy\n1. **Low mental overhead**   \n Realistically, most Python programmers that wish to write packages need to have some\n familiarity with the Python package development model, including the conventional\nstructure of a package. For this reason, I feel that it is important to design\n`literary` such that these skills translate directly to designing libraries with\nnotebooks\n2. **Minimal downstream impact**  \n Users of `literary` packages should not realise that they are consuming \n notebook-generated code at runtime. This means that a pure-Python package needs to\n be generated from the notebooks, and it must use the conventional import model. For\n this reason, `literary` should only exist as a development dependency of\n the package.\n  \n\n## Differences with `nbdev`\n* Use of cell tags instead of comments or magics to dictate exports\n* Use of `nbconvert` machinery to build the pure-Python lib package\n* Use of import hooks to import other notebooks\n    * Maintains a similar programming model to conventional module\n development\n    * Reduces the need to modify notebook contents during conversion \n* Minimal runtime overhead\n    * Features like `patch` are removed from the generated module (& imported notebook source) using AST transformations\n* Currently no documentation generation\n    * Loosely, the plan is to use existing notebook-book tooling to re-use the\n     existing Jupyter ecosystem\n\n\n## Differences with Knuth\nKnuth introduced the `tangle` and `weave` programs to produce separate documentation and source code for compilation. \nLiterary differs in treating the notebook as the "ground truth" for documentation + testing, and generating smaller source code for packaging.\n\n\n## Design\nThe plan for this package is:\n1. Notebooks will be written inside `<PACKAGE_NAME>/` in literary project\'s root directory\n2. Notebooks will respect relative imports and other pure-Python features to minimise the differences between the generated packages and the notebooks\n3. A pure-python generated `lib/<PACKAGE_NAME>/` directory will be built before Poetry builds the final project.   \n  E.g. \n    ```toml\n    [tool.poetry]\n    # ...\n    packages = [\n      { include = "<PACKAGE_NAME>", from = "lib" },\n    ]\n    ```\n',
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agoose77/literary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

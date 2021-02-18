# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aim_build']

package_data = \
{'': ['*']}

install_requires = \
['cerberus>=1.3,<2.0',
 'ninja-syntax>=1.7,<2.0',
 'tabulate>=0.8.7,<0.9.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['aim = aim_build.main:entry']}

setup_kwargs = {
    'name': 'aim-build',
    'version': '0.1.25',
    'description': 'A powerful and easy to use build tool for C++.',
    'long_description': '<p align="center">\n<img src="https://github.com/diwalkerdev/Assets/blob/master/Aim/aim.png" width="300" height="300">\n</p>\n\n![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/diwalkerdev/aim?include_prereleases)\n![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/diwalkerdev/aim/latest/dev?include_prereleases)\n![Python package](https://github.com/diwalkerdev/Aim/workflows/Python%20package/badge.svg?branch=dev)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aim-build)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/aim-build)\n![GitHub contributors](https://img.shields.io/github/contributors/diwalkerdev/aim)\n![GitHub](https://img.shields.io/github/license/diwalkerdev/aim)\n\n# Aim\nAim is a command line tool for building C++ projects. \n\nProject goals:\n * Simplify building C++ projects\n * Clear, easy to understand mechanism for supporting different **build targets**\\*\n * Rapid dependency resolution and builds provided by [ninja](https://ninja-build.org/)\n * Easy to use - builds are managed using a `toml` file\n\n\\* A **build target** is some combination of _things_ that affects the output binary. See Methodology for more information.\n\nSee [ShapeAttack](https://github.com/diwalkerdev/ShapeAttack), for a demo of how Aim can be used in a real world example.\n\n\n## Known Limitations\n* Windows support is still in development.\n\n\n## Why another build tool?\nAim is an attempt to make building C++ projects as simple as possible. It is very easy to add libraries and other executables to a project. Other build tools seem overly complex and require users to learn new sytaxes. \n\nWith Aim:\n* adding build targets is simple and explicit\n* all builds occur in their own directory by default\n* builds are fast and reliable executed by the `ninja` build system.\n\nAll you have to do is write the `target.toml` file. It is very easy.\n\n\n## Methodology\nAim treats any build variation as its own unique build target. A build target is some combination of _things_ that affects the output binary. This could be variations of:\n * operating system (Windows, OSX, Gnu Linux)\n * compiler (MSVC, GCC, Clang)\n * build type (Release, Debug, Sanitized)\n * and maybe more. \n \n Each build target has its own name, which is just some unique identifier that may comprise of the \'parts\' that make up the build. For example, the build target `linux-clang++-release` indicates that this is a `release` build, using the `clang++` compiler for the `linux` operating system.\n\nSupport for a build target is added by writing a `target.toml` file in a build directory. Each `target.toml` file must be written out in full for each target that you need to support. There is no way for target files to share information or to depend on another. While this leads to duplication between target files, it makes them very explicit and makes debugging builds much easier.\n\nA target file can contain a number of builds. Each build could be a part of the project that builds as static or dyanamic library or as an executable. A build in the `target.toml` file will look roughly like:\n```\n[[builds]]\n    name = "exe"                        # the unique name for this build.\n    buildRule = "exe"                   # the type of build, in this case an executable. But can also be staticlib or dynamiclib.\n    requires = ["lib_adder"]            # the name of a build also built by Aim. Must be library.\n    outputName = "the_calculator"       # the output name, which is either the executable name or the library name.\n    srcDirs = ["src"]                   # the src directories to build the executable library from.\n    includePaths = ["include"]          # additional include paths to use during the build.\n```\nThere are additional options depending on the `buildRule`. For a complete list of options see `schema.py`.\n\nWhen a build is executed, all artifacts are placed in the target\'s build directory. This keeps your source directory clean and free of clutter.\n\n\n## Getting Started\n### Prerequisites\nAim requires the following dependencies:\n* [python](https://www.python.org/) - version 3.7 or above.\n* [ninja](https://ninja-build.org/)\n* [poetry](https://python-poetry.org/) - for development only\n\n### Installation\nAim is a `python` project and is installed using `pip`.\n\n```\npip install --user aim-build\n```\n\n### Using\n\n<img src="https://github.com/diwalkerdev/Assets/blob/master/Aim/aim-init-demo.gif?raw=true" width="600px">\n\nNote, `aim init` has an optional flag `--demo`. This adds some simple source files to the project for demonstration purposes.\n\nThere are 3 main commands:\n* `list` - Displays the builds for the target\n* `init` - Creates a project structure\n* `build` - Executes a build\n\nFor more information run:\n```\naim <command> --help\n```\n\n## Developing Aim\n\nAim is a Python project and uses the [poetry](https://python-poetry.org/) dependency manager. See [poetry installation](https://python-poetry.org/docs/#installation) for instructions.\n\nOnce you have cloned the project, the virtual environment and dependencies can be installed simply by executing:\n\n```\npoetry install\n```\n\n### Dev Install\nUnfortunately, unlike `setuptools`, there is no means to do a \'dev install\' using poetry. A dev install causes a command line script to use the current development code which is useful so a project does not need to be reinstalled after every modification. \n\nIn order to use Aim on the command line, is it recommended to create an alias. The alias needs to:\n* adds Aim to `PYTHONPATH` to resolve import/module paths \n* execute the main Aim script using virtualenv\'s python\n\nFor `bash` this looks like:\n```\nalias aim="PYTHONPATH=$PWD/src $(poetry env info -p)/bin/python $PWD/src/aim_build/main.py"\n```\n\nFor `fish` shell this looks like:\n```\nalias aim="PYTHONPATH=$PWD/src "(poetry env info -p)"/bin/python $PWD/src/aim_build/main.py"\n```\n\n## Other remarks\nThe target file can be extended with other builds. For example to add unit tests. Begin by partitioning any code that\nneeds to be tested into a library. Then create another build for the test. Since unit tests are really an executable,\nset `buildRule="exe"` and add the library to the `requires` list. Remember to update the build for the primary\nexecutable as well if you have one.\n\nThe unit tests can now be built and run like any other executable.\n\n## Future improvements / known limitations\n * The `cc` field isn\'t actually used at the moment. All build steps are performed by the cxx compiler.\n',
    'author': 'David Walker',
    'author_email': 'diwalkerdev@twitter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diwalkerdev/Aim',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

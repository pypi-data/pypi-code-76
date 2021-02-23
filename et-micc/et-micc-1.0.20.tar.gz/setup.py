# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_micc']

package_data = \
{'': ['*'],
 'et_micc': ['templates/app-simple/{{cookiecutter.project_name}}/tests/*',
             'templates/app-simple/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/*',
             'templates/app-sub-commands/{{cookiecutter.project_name}}/tests/*',
             'templates/app-sub-commands/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/*',
             'templates/module-cpp/{{cookiecutter.project_name}}/tests/*',
             'templates/module-cpp/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/cpp_{{cookiecutter.module_name}}/*',
             'templates/module-f90/{{cookiecutter.project_name}}/tests/*',
             'templates/module-f90/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/f90_{{cookiecutter.module_name}}/*',
             'templates/module-py/{{cookiecutter.project_name}}/tests/*',
             'templates/module-py/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/*',
             'templates/package-base/hooks/*',
             'templates/package-base/{{cookiecutter.project_name}}/*',
             'templates/package-base/{{cookiecutter.project_name}}/tests/*',
             'templates/package-general-docs/hooks/*',
             'templates/package-general-docs/{{cookiecutter.project_name}}/*',
             'templates/package-general-docs/{{cookiecutter.project_name}}/docs/*',
             'templates/package-general/hooks/*',
             'templates/package-general/{{cookiecutter.project_name}}/{{cookiecutter.package_name}}/*',
             'templates/package-simple-docs/hooks/*',
             'templates/package-simple-docs/{{cookiecutter.project_name}}/*',
             'templates/package-simple-docs/{{cookiecutter.project_name}}/docs/*',
             'templates/package-simple/hooks/*',
             'templates/package-simple/{{cookiecutter.project_name}}/*']}

install_requires = \
['click>=7.0,<8.0',
 'cookiecutter>=1.6.0,<2.0.0',
 'pypi-simple>=0.8.0,<0.9.0',
 'semantic_version>=2.8.3,<3.0.0',
 'sphinx-click>=2.3.0,<3.0.0',
 'sphinx-rtd-theme>=0.4.3,<0.5.0',
 'tomlkit>=0.5.8,<0.6.0',
 'walkdir>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['micc = et_micc:cli_micc.main']}

setup_kwargs = {
    'name': 'et-micc',
    'version': '1.0.20',
    'description': 'A practical Python project skeleton generator.',
    'long_description': "****\nMicc\n****\n\n.. image:: https://img.shields.io/pypi/v/micc.svg\n        :target: https://pypi.python.org/pypi/micc\n\n.. image:: https://img.shields.io/travis/etijskens/micc.svg\n        :target: https://travis-ci.org/etijskens/micc\n\n.. image:: https://readthedocs.org/projects/micc/badge/?version=latest\n        :target: https://micc.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n`Micc <https://github.com/etijskens/et-micc>`_ is a Python project manager: it helps \nyou organize your Python project from simple single file modules to fully fledged \nPython packages containing modules, sub-modules, apps and binary extension modules \nwritten in Fortran or C++. Micc_ organizes your project in a way that is considered good\npractice by a large part of the Python community. \n\n* Micc_ helps you create new projects. You can start small with a simple one-file \n  package and add material as you go, such as:\n  \n  * Python **sub-modules** and **sub-packages**,\n  * **applications**, also known as command line interfaces (CLIs). \n  * **binary extension modules** written in C++ and Fortran. Boiler plate code is \n    automatically added as to build these binary extension with having to go through\n    al the details. This is, in fact, the foremost reason that got me started on this\n    project: For *High Performance Python* it is essential to rewrite slow and \n    time consuming parts of a Python script or module in a language that is made \n    for High Performance Computing. As figuring out how that can be done, requires \n    quite some effort, Micc_ was made to automate this part while maintaining the \n    flexibility. \n  * Micc_ adds typically files containing example code to show you how to add your\n    own functionality.\n    \n* You can automatically **extract documentation** from the doc-strings of your files,\n  and build html documentation that you can consult in your browser, or a .pdf \n  documentation file.\n* With a little extra effort the generated html **documentation is automatically published** \n  to `readthedocs <https://readthedocs.org>`_.\n* Micc_ helps you with **version management and control**.\n* Micc_ helps you with **testing** your code.\n* Micc_ helps you with **publishing** your code to e.g. `PyPI <https://pypi.org>`_, so\n  that you colleagues can use your code by simply running::\n\n    > pip install your_nifty_package\n\nCredits\n-------\nMicc_ does not do all of this by itself. For many things it relies on other strong \nopen source tools and it is therefor open source as well (MIT Licence). Here is a list \nof tools micc_ is using or cooperating with happily:\n\n*   `Pyenv <https://github.com/pyenv/pyenv>`_: management of different Python versions.\n*   `Pipx <https://github.com/pipxproject/pipx/>`_ for installation of CLIs in a system-wide\n    way.\n*   `Poetry <https://github.com/sdispater/poetry>`_ for dependency management, virtual\n    environment management, packaging and publishing.\n*   `Git <https://www.git-scm.com/>`_ for version control.\n*   `CMake <https://cmake.org>`_ is usde for building binary extension modules written\n    in C++.\n\nThe above tools are not dependencies of Micc_ and must be installed separately. Then\nthere are a number of python packages on which micc_ depends and which are automatically\ninstalled when poetry_ creates a virtual environment for a project.\n\n*   `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ for creating boilerplate\n    code from templates for all the parts that can be added to your project.\n*   `Python-semanticversion <https://github.com/rbarrois/python-semanticversion/blob/master/docs/index.rst>`_\n    for managing version strings and dependency version constraints according to the\n    `Semver 2.0 <http://semver.org/>`_ specification.\n*   `Pytest <https://www.git-scm.com/>`_ for testing your code.\n*   `Click <https://click.palletsprojects.com/en/7.x/>`_ for a pythonic and intuitive definition\n    of command-line interfaces (CLIs).\n*   `Sphinx <http://www.sphinx-doc.org/>`_ to extract documentation from your project's\n    doc-strings.\n*   `Sphinx-click <https://sphinx-click.readthedocs.io/en/latest/>`_ for extracting documentation\n    from the click_ command descriptions.\n*   `F2py <https://docs.scipy.org/doc/numpy/f2py/>`_ for transforming modern Fortran code into performant\n    binary extension modules interfacing nicely with `Numpy <https://numpy.org/>`_.\n*   `Pybind11 <https://pybind11.readthedocs.io/en/stable/>`_ as the\n    glue between C++ source code and performant binary extension modules, also interfacing nicely with Numpy_.\n\nRoadmap\n=======\nThese features are still on our wish list:\n\n* Deployment on the `VSC <https://www.vscentrum.be>`_ clusters\n* Contininous integtration (CI)\n* Code style, e.g. `flake8 <http://flake8.pycqa.org/en/latest/>`_ or `black <https://github.com/psf/black>`_\n* Profiling\n\n",
    'author': 'Engelbert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-micc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

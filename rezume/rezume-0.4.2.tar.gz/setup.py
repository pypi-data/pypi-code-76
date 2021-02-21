# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rezume', 'rezume.cli', 'rezume.cli.commands', 'rezume.cli.commands.serve']

package_data = \
{'': ['*'], 'rezume': ['assets/*']}

install_requires = \
['pydantic[email]>=1.7.3,<2.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['rezume = rezume.cli:main']}

setup_kwargs = {
    'name': 'rezume',
    'version': '0.4.2',
    'description': 'Rezume, validate and create text-based resumes easily.',
    'long_description': "rezume\n======\n\nRezume is a Python library to validate and easily create a `YAML <https://yaml.org>`_\nbased resume file that is `JSON Resume <https://jsonresume.org>`_ compatible according to\nthe `defined schema <https://jsoonresume.org/schema>`_.\n\n\nInstallation\n------------\n\nInstall from `Pypi <https://pypi.org/project/rezume/>`_ by running this command:\n\n.. code-block:: bash\n\n    pip install rezume\n\n\nDependencies\n^^^^^^^^^^^^\n\nRezume requires Python 3.6+ and depends mainly on `pydantic <https://pypi.org/project/pydandic>`_\nfor data validation and `pyyaml <https://pypi.org/project/>`_ for processing YAML data.\n\n\nUsage\n-----\n\nYou can use ``rezume`` as a Python package as shown below:\n\n.. code-block:: python\n\n    from rezume import RezumeError, Rezume\n\n    # sample (invalid) rezume data to validate\n    rezume_data = { name: 'John Doe' }\n\n    # check the validity of sample data\n    if Rezume.is_valid(rezume_data):\n        print('Validated successfully!')\n    else:\n        print('Invalid rezume')\n\n    # alternatively, if we prefer catching exceptions\n    try:\n        Rezume.validate(rezume_data)\n        print('Validated successfully!')\n    except RezumeError as ex:\n        print(f'Invalid rezume: {ex}')\n\n\nTo validate a rezume file instead:\n\n.. code-block:: python\n\n    from pathlib import Path\n    from rezume import RezumeError, Rezume\n\n    # path to sample file to validate\n    rezume_file = Path('/path/to/sample/rezume-file.yml')\n\n    # use\n    Rezume.is_valid(rezume_file)    # returns boolean\n\n    # or\n    Rezume.validate(rezume_file)    # throws exception if invalid\n\n\nFurthermore, you can programmatically process a Rezume:\n\n.. code-block:: python\n\n    import json\n    from pathlib import Path\n    from rezume import RezumeError, Rezume\n\n    # load and modify a standard JSON resume\n\n    rezume = Rezume()\n\n    json_file = Path('/path/to/json/resume-file.json')\n    with json_file.open('r') as fp:\n        data = json.load(fp)\n        rezume.load_data(data)   # throws exception if invalid\n\n    rezume.basics.name = 'John Doe (Verified)'\n    print(rezume.dump_data())\n\n\n    # or programmatically modify a YAML rezume file\n\n    yaml_file = Path('/path/to/yaml/rezume-file.yml')\n    try:\n        rezume = Rezume()\n        rezume.load(yaml_file)  # throws exception if invalid\n    except RezumeError:\n        print('Unable to process rezume file')\n    else:\n        rezume.basics.label = 'Pythonista'\n        print(rezume.dump_data())\n\n\nIn addition, ``rezume`` can be used as a command line tool to create or validate\na YAML-based rezume file. Here is the output of ``rezume --help``\n\n.. code-block:: bash\n\n    Usage: rezume [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --install-completion  Install completion for the current shell.\n      --show-completion     Show completion for the current shell, to copy it or\n                              customize the installation.\n\n      --help                Show this message and exit.\n\n    Commands:\n      init   Initializes a new rezume.yml file\n      serve  Serves a rezume for local viewing applying available themes\n      test   Validates correctness of a rezume.yml file\n\n\nLicense\n-------\n\nThis project is licensed under the `BSD license <LICENSE>`_\n",
    'author': 'Abdul-Hakeem Shaibu',
    'author_email': 's.abdulhakeeem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hkmshb/rezume.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

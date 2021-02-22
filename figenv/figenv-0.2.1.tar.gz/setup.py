# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['figenv']
setup_kwargs = {
    'name': 'figenv',
    'version': '0.2.1',
    'description': 'Metaclass for handling configuration class objects using environment variables',
    'long_description': "Figenv\n======\n\n.. image:: https://github.com/gtmanfred/figenv/workflows/Tests/badge.svg\n    :target: https://github.com/gtmanfred/figenv\n\n.. image:: https://img.shields.io/codecov/c/github/gtmanfred/figenv\n    :target: https://codecov.io/gh/gtmanfred/figenv\n\n.. image:: https://img.shields.io/pypi/v/figenv\n    :target: https://pypi.org/project/figenv\n\n.. image:: https://img.shields.io/pypi/l/figenv\n    :target: http://www.apache.org/licenses/LICENSE-2.0\n\n.. image:: https://img.shields.io/pypi/dm/figenv\n    :target: https://pypi.org/project/figenv/\n\nMetaclass for handling configuration class objects using environment variables.\n\nIf an environment variable is specified, the metaclass will pull the variable\nfrom the environment, the variable defined on the class will be used.\n\nThis was built to be a dropin replacement for `flask-env\n<https://pypi.org/project/Flask-Env/>`_ but supporting change environment\nvariables after the meta class is loaded.\n\nConfig\n------\n\nThere are 2 configuration options, that are set on the base class object.\n\n``ENV_LOAD_ALL = <True/False>``\n\n   Setting this on the class will allow loading any environment variable even\n   if it is not set on the base class.\n\n``ENV_PREFIX = <string>``\n\n   Setting this will will be a prefix for variables in the environment.\n\nInstall\n-------\n\nThis should just be pip installed\n\n.. code-block:: bash\n\n   python3 -m pip install figenv\n\nUsage\n-----\n\nThe basic usecase is below.\n\n.. code-block:: python\n\n    import os\n\n    import figenv\n\n    class Config(metaclass=figenv.MetaConfig):\n\n        ENV_LOAD_ALL = True\n        ENV_PREFIX = 'ROCKSTEADY_'\n\n        BLAH = True\n        TIMEOUT = 5\n        POSTGRES_HOST = 'localhost'\n        POSTGRES_PORT = 5432\n        POSTGRES_USER = 'bebop'\n        POSTGRES_PASS = 'secret'\n        POSTGRES_DB = 'main'\n\n        def SQLALCHEMY_DATABASE_URI(cls):\n            return 'postgresql://{user}:{secret}@{host}:{port}/{database}?sslmode=require'.format(\n                user=cls.POSTGRES_USER,\n                secret=cls.POSTGRES_PASS,\n                host=cls.POSTGRES_HOST,\n                port=cls.POSTGRES_PORT,\n                database=cls.POSTGRES_DATABASE,\n            )\n\n   assert Config.TIMEOUT == 5\n   assert Config.BLAH is True\n   assert Config.SQLALCHEMY_DATABASE_URI == 'postgresql://bebop:secret@localhost:5432/public?sslmode=require'\n   try:\n       Config.WHAT\n   except AttributeError:\n       pass\n\n   os.environ.update({\n       'ROCKSTEADY_BLAH': 'false',\n       'ROCKSTEADY_TIMEOUT': '15',\n       'ROCKSTEADY_WHAT': '2.9',\n       'ROCKSTEADY_SQLALCHEMY_DATABASE_URI': 'postgres://localhost:5432/db',\n   })\n\n   assert Config.TIMEOUT == 15\n   assert Config.BLAH is False\n   assert Config.WHAT == 2.9\n   assert Config.SQLALCHEMY_DATABASE_URI == 'postgres://localhost:5432/db'\n",
    'author': 'Daniel Wallace',
    'author_email': 'daniel@gtmanfred.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gtmanfred/figenv',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictionaryutils']

package_data = \
{'': ['*'], 'dictionaryutils': ['schemas/*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'cdislogging>=1.0.0,<2.0.0',
 'jsonschema>=2.5,<4.0',
 'requests>=2.18,<3.0']

setup_kwargs = {
    'name': 'dictionaryutils',
    'version': '3.4.1',
    'description': 'Python wrapper and metaschema for datadictionary.',
    'long_description': '# dictionaryutils\n\npython wrapper and metaschema for datadictionary.\nIt can be used to:\n- load a local dictionary to a python object.\n- dump schemas to a file that can be uploaded to s3 as an artifact.\n- load schema file from an url to a python object that can be used by services\n\n## Test for dictionary validity with Docker\nSay you have a dictionary you are building locally and you want to see if it will pass the tests.\n\nYou can add a simple alias to your `.bash_profile` to enable a quick test command:\n```\ntestdict() { docker run --rm -v $(pwd):/dictionary quay.io/cdis/dictionaryutils:master; }\n```\n\nThen from the directory containing the `gdcdictionary` directory run `testdict`.\n\n\n## Generate simulated data with Docker\nIf you wish to generate fake simulated data you can also do that with dictionaryutils and the data-simulator.\n\n```\nsimdata() { docker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "cd /dictionary && python setup.py install --force; python /src/datasimulator/bin/data-simulator simulate --path /simdata/ $*; export SUCCESS=$?; rm -rf build dictionaryutils dist gdcdictionary.egg-info; chmod -R a+rwX /simdata; exit $SUCCESS"; }\nsimdataurl() { docker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "python /src/datasimulator/bin/data-simulator simulate --path /simdata/ $*; chmod -R a+rwX /simdata"; }\n\n```\n\nThen from the directory containing the `gdcdictionary` directory run `simdata` and a folder will be created called `simdata` with the results of the simulator run. You can also pass in additional arguments to the data-simulator script such as `simdata --max_samples 10`.\n\nThe `--max_samples` argument will define a default number of nodes to simulate, but you can override it using the `--node_num_instances_file` argument. For example, if you create the following `instances.json`:\n\n```\n{\n        "case": 100,\n        "demographic": 100\n}\n\n```\nThen run the following:\n```\ndocker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "cd /dictionary && python setup.py install --force; python /src/datasimulator/bin/data-simulator simulate --path /simdata/ --program workshop --project project1 --max_samples 10 --node_num_instances_file instances.json; export SUCCESS=$?; rm -rf build dictionaryutils dist gdcdictionary.egg-info; chmod -R a+rwX /simdata; exit $SUCCESS";\n```\nThen you\'ll get 100 each of `case` and `demographic` nodes and 10 each of everything else. Note that the above example also defines `program` and `project` names.\n\nYou can also run the simulator for an arbitrary json url by using `simdataurl --url https://datacommons.example.com/schema.json`.\n\n\n## Use dictionaryutils to load a dictionary\n```\nfrom dictionaryutils import DataDictionary\n\ndict_fetch_from_remote = DataDictionary(url=URL_FOR_THE_JSON)\n\ndict_loaded_locally = DataDictionary(root_dir=PATH_TO_SCHEMA_DIR)\n```\n\n## Use dictionaryutils to dump a dictionary\n```\nimport json\nfrom dictionaryutils import dump_schemas_from_dir\n\nwith open(\'dump.json\', \'w\') as f:\n    json.dump(dump_schemas_from_dir(\'../datadictionary/gdcdictionary/schemas/\'), f)\n```\n',
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uc-cdis/dictionaryutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)

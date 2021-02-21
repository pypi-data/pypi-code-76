# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdpcli', 'pdpcli.commands', 'pdpcli.configs', 'pdpcli.data', 'pdpcli.stages']

package_data = \
{'': ['*']}

install_requires = \
['colt>=0.6.1,<0.7.0',
 'jsonnet>=0.17.0,<0.18.0',
 'nltk>=3.5,<4.0',
 'omegaconf>=2.0.6,<3.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pdpipe>=0.0.53,<0.0.54',
 'scikit-learn>=0.24.1,<0.25.0']

entry_points = \
{'console_scripts': ['pdp = pdpcli.__main__:run']}

setup_kwargs = {
    'name': 'pdpcli',
    'version': '0.2.0',
    'description': 'PdpCLI is a pandas DataFrame processing CLI tool which enables you to build a pandas pipeline from a configuration file.',
    'long_description': 'PdpCLI\n======\n\n[![Actions Status](https://github.com/altescy/pdpcli/workflows/CI/badge.svg)](https://github.com/altescy/pdpcli/actions?query=workflow%3ACI)\n[![Python version](https://img.shields.io/pypi/pyversions/pdpcli)](https://github.com/altescy/pdpcli)\n[![PyPI version](https://img.shields.io/pypi/v/pdpcli)](https://pypi.org/project/pdpcli/)\n[![License](https://img.shields.io/github/license/altescy/pdpcli)](https://github.com/altescy/pdpcli/blob/master/LICENSE)\n\n### Quick Links\n\n- [Introduction](#Introduction)\n- [Installation](#Installation)\n- [Tutorial](#Tutorial)\n  - [Basic Usage](#basic-usage)\n  - [Data Reader / Writer](#data-reader--writer)\n  - [Plugins](#plugins)\n\n\n## Introduction\n\nPdpCLI is a pandas DataFrame processing CLI tool which enables you to build a pandas pipeline powered by [pdpipe](https://pdpipe.github.io/pdpipe/) from a configuration file. You can also extend pipeline stages and data readers/ writers by using your own python scripts.\n\n### Features\n  - Process pandas DataFrame from CLI without wrting Python scripts\n  - Support multiple configuration file formats: YAML, JSON, Jsonnet\n  - Read / write data files in the following formats: CSV, TSV, JSONL, XLSX\n  - Extensible pipeline and data readers / writers\n\n\n## Installation\n\nInstalling the library is simple using pip.\n```\n$ pip install pdpcli\n```\n\n\n## Tutorial\n\n### Basic Usage\n\n1. Write a pipeline config file `config.yml` like below. The `type` fields under `pipeline` correspond to the snake-cased class names of the [`PdpipelineStages`](https://pdpipe.github.io/pdpipe/doc/pdpipe/#types-of-pipeline-stages). The other fields such as `stage` and `columns` specify the parameters of the `__init__` methods of the corresponging classes. Internally, this configuration file is converted to Python objects by [`colt`](https://github.com/altescy/colt).\n\n```yaml\npipeline:\n  type: pipeline\n  stages:\n    drop_columns:\n      type: col_drop\n      columns: foo\n\n    encode:\n      type: one_hot_encode\n      columns: sex\n\n    tokenize:\n      type: tokenize_text\n      columns: profile\n\n    vectorize:\n      type: tfidf_vectorize_token_lists\n      column: profile\n```\n\n2. Build a pipeline by training on `train.csv`. The following command generage a pickled pipeline file `pipeline.pkl` after training.\n```\n$ pdp build config.yml pipeline.pkl --input-file train.csv\n```\n\n3. Apply fitted pipeline to `test.csv` and get output of the processed file `processed_test.jsonl` by the following command. PdpCLI automatically detects the output file format based on the file name. In the following example, processed DataFrame will be exported as the JSONL format.\n```\n$ pdp apply pipeline.pkl test.csv --output-file processed_test.jsonl\n```\n\n4. You can also directly run the pipeline from a config file if you don\'t need to fit the pipeline.\n```\n$ pdp apply config.yml test.csv --output-file processed_test.jsonl\n```\n\n5. It is possible to change parameters via command line:\n```\npdp apply.yml test.csv pipeline.stages.drop_columns.column=age\n```\n\n### Data Reader / Writer\n\n\n### Plugins\n\nBy using plugins, you can extend PdpCLI. The plugin feature enables you to use your own pipeline stages, data reader / writer and commands.\n\n#### Add a new stage\n\n1. Write your plugin script `mypdp.py` like the following. `PrintStage` just shows the DataFrame on stdout.\n```python\nimport pdpcli\n\n@pdpcli.PdPipelineStage.register("print")\nclass PrintStage(pdpcli.PdPipelineStage):\n    def _prec(self, df):\n        return True\n\n    def _transform(self, df, verbose):\n        print(df.to_string(index=False))\n        return df\n```\n\n2. Update `config.yml` to use your plugin.\n```yml\npipeline:\n    type: pipeline\n    stages:\n        drop_columns:\n        ...\n        \n        print:\n            type: print\n            \n        encode:\n        ...\n```\n\n2. Execute command with `--module mypdp` and you can see the DataFrame after `drop_columns`.\n```\n$ pdp apply config.yml test.csv --module mypdp\n```\n\n#### Add a new command\n\nYou can also add new coomands not only stages.\n\n1. Add the following script to `mypdp.py`. This `greet` command prints out a greeting message with your name.\n```python\n@pdpcli.Subcommand.register(\n    name="greet",\n    description="say hello",\n    help="say hello",\n)\nclass GreetCommand(pdpcli.Subcommand):\n    requires_plugins = False\n\n    def set_arguments(self):\n        self.parser.add_argument("--name", default="world")\n\n    def run(self, args):\n        print(f"Hello, {args.name}!")\n\n```\n\n2. To register this command, you need to create the`.pdpcli_plugins` file. Due to the module import order, the `--module` option is unavailable for command registration.\n```\n$ echo "mypdp" > .pdpcli_plugins\n```\n\n3. Run the following command and get the message like below. By using the `.pdpcli_plugins` file, it is unnecessary to enter the `--module` option for each execution.\n```\n$ pdp greet --name altescy\nHello, altescy\n```\n',
    'author': 'altescy',
    'author_email': 'altescy@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/altescy/pdpcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

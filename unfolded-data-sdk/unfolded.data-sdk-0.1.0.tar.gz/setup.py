# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_sdk']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'pydantic>=1.7.0,<2.0.0', 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['uf-data-sdk = unfolded.data_sdk.cli:main']}

setup_kwargs = {
    'name': 'unfolded.data-sdk',
    'version': '0.1.0',
    'description': "Module for working with Unfolded Studio's Data SDK",
    'long_description': "# `unfolded-data-sdk`\n\nPython package for interfacing with Unfolded's Data SDK.\n\n## Installation\n\nFor now, this package is not on a public Python package repository. However you\ncan install it directly from Github easily as long as you have access to the\nrepository:\n\n```\npip install git+ssh://git@github.com/UnfoldedInc/unfolded-py.git#subdirectory=modules/data-sdk\n```\n\n## Usage\n\n### CLI\n\nThe CLI is available through `uf-data-sdk` on the command line. Running that\nwithout any other arguments gives you a list of available commands:\n\n```\n> uf-data-sdk\nUsage: uf-data-sdk [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  delete-dataset    Delete dataset from Unfolded Studio Warning: This...\n  download-dataset  Download existing dataset to disk\n  list-datasets     List datasets for a given user\n  update-dataset    Update data for existing Unfolded Studio dataset\n  upload-file       Upload new dataset to Unfolded Studio\n```\n\nThen to see how to use a command, pass `--help` to a subcommand:\n\n```\n> uf-data-sdk list-datasets --help\nUsage: uf-data-sdk list-datasets [OPTIONS]\n\n  List datasets for a given user\n\nOptions:\n  --token TEXT    Unfolded Studio access token.  [required]\n  --baseurl TEXT  Unfolded Studio API URL.  [default: https://api.unfolded.ai]\n  --help          Show this message and exit.\n```\n\n### Python Package\n\nThe Python package can be imported via `unfolded.data_sdk`:\n\n```py\nfrom unfolded.data_sdk import DataSDK, ContentType\n\ndata_sdk = DataSDK(token='eyJ...')\n```\n\n#### List Datasets\n\nList datasets for given user\n\n```py\ndatasets = data_sdk.list_datasets()\n```\n\n#### Get Dataset by ID\n\nGet dataset given its id\n\n```py\ndataset = datasets[0]\ndata_sdk.get_dataset_by_id(dataset)\n```\n\n#### Download dataset data\n\nDownload data for dataset given its id\n\n```py\ndataset = datasets[0]\ndata_sdk.download_dataset(dataset, output_file='output.csv')\n```\n\n#### Upload new dataset\n\nUpload new dataset to Unfolded Studio\n\n```py\ndata_sdk.upload_file(\n    file='new_file.csv',\n    name='Dataset name',\n    content_type=ContentType.CSV,\n    description='Dataset description')\n```\n\n#### Update existing dataset\n\nUpdate data for existing Unfolded Studio dataset\n\n```py\ndataset = datasets[0]\ndata_sdk.update_dataset(\n    file='new_file.csv',\n    dataset=dataset,\n    content_type=ContentType.CSV)\n```\n\n#### Delete dataset\n\nDelete dataset from Unfolded Studio\n\n**Warning: This operation cannot be undone.** If you delete a dataset\ncurrently used in one or more maps, the dataset will be removed from\nthose maps, possibly causing them to render incorrectly.\n\n```py\ndataset = datasets[0]\ndata_sdk.delete_dataset(dataset)\n```\n",
    'author': 'Kyle Barron',
    'author_email': 'kyle@unfolded.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)

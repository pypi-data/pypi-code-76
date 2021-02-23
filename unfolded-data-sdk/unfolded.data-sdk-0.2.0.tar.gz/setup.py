# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_sdk']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.0.0,<3.0.0',
 'click>=7.0.0,<8.0.0',
 'pydantic>=1.7.0,<2.0.0',
 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['uf-data-sdk = unfolded.data_sdk.cli:main']}

setup_kwargs = {
    'name': 'unfolded.data-sdk',
    'version': '0.2.0',
    'description': "Module for working with Unfolded Studio's Data SDK",
    'long_description': "# `unfolded.data-sdk`\n\nPython package for interfacing with Unfolded's Data SDK.\n\n## Installation\n\nInstall via pip:\n\n```\npip install -U unfolded.data-sdk\n```\n\n## Authentication\n\nBefore using the Data SDK, you must authenticate. Authentication with a refresh\ntoken only needs to be done once, and can be done either through the CLI or\nPython module. First go to\n[studio.unfolded.ai/tokens.html](https://studio.unfolded.ai/tokens.html) to sign\nin. Then copy the **Refresh Token** for use in the next step.\n\n### CLI\n\nTo authenticate via the CLI, use the `store-refresh-token` method:\n\n```\n> uf-data-sdk store-refresh-token\n```\n\nThe CLI will then prompt for your refresh token, and print a message when it has\nsuccessfully stored it.\n\n### Python module\n\nTo authenticate via the Python module, pass the refresh token to the `DataSDK`\nclass. **This only needs to happen once.** For future uses of the `DataSDK`\nclass, do not pass a `refresh_token` argument.\n\n```py\nfrom unfolded.data_sdk import DataSDK\nDataSDK(refresh_token='v1.ABC...')\n```\n\n## Usage\n\n### CLI\n\nThe CLI is available through `uf-data-sdk` on the command line. Running that\nwithout any other arguments gives you a list of available commands:\n\n```\n> uf-data-sdk\nUsage: uf-data-sdk [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  delete-dataset       Delete dataset from Unfolded Studio Warning: This...\n  download-dataset     Download data for existing dataset to disk\n  list-datasets        List datasets for a given user\n  store-refresh-token  Store refresh token to enable seamless future...\n  update-dataset       Update data for existing Unfolded Studio dataset\n  upload-file          Upload new dataset to Unfolded Studio\n```\n\nThen to see how to use a command, pass `--help` to a subcommand:\n\n```\n> uf-data-sdk download-dataset --help\n\nUsage: uf-data-sdk download-dataset [OPTIONS]\n\n  Download data for existing dataset to disk\n\nOptions:\n  --dataset-id TEXT       Dataset id.  [required]\n  -o, --output-file PATH  Output file for dataset.  [required]\n  --help                  Show this message and exit.\n```\n\n### Python Package\n\nThe Python package can be imported via `unfolded.data_sdk`:\n\n```py\nfrom unfolded.data_sdk import DataSDK, MediaType\n\ndata_sdk = DataSDK()\n```\n\n#### List Datasets\n\nList datasets for given user\n\n```py\ndatasets = data_sdk.list_datasets()\n```\n\n#### Get Dataset by ID\n\nGet dataset given its id\n\n```py\ndataset = datasets[0]\ndata_sdk.get_dataset_by_id(dataset)\n```\n\n#### Download dataset data\n\nDownload data for dataset given its id\n\n```py\ndataset = datasets[0]\ndata_sdk.download_dataset(dataset, output_file='output.csv')\n```\n\n#### Upload new dataset\n\nUpload new dataset to Unfolded Studio\n\n```py\ndata_sdk.upload_file(\n    file='new_file.csv',\n    name='Dataset name',\n    media_type=MediaType.CSV,\n    description='Dataset description')\n```\n\n#### Update existing dataset\n\nUpdate data for existing Unfolded Studio dataset\n\n```py\ndataset = datasets[0]\ndata_sdk.update_dataset(\n    file='new_file.csv',\n    dataset=dataset,\n    media_type=MediaType.CSV)\n```\n\n#### Delete dataset\n\nDelete dataset from Unfolded Studio\n\n**Warning: This operation cannot be undone.** If you delete a dataset\ncurrently used in one or more maps, the dataset will be removed from\nthose maps, possibly causing them to render incorrectly.\n\n```py\ndataset = datasets[0]\ndata_sdk.delete_dataset(dataset)\n```\n\n### DataFrame support\n\nThe Python package makes it simple to upload pandas `DataFrames` and geopandas\n`GeoDataFrames` to Unfolded Studio. Pass either a `DataFrame` or a\n`GeoDataFrame` to `upload_dataframe`:\n\n```py\nimport pandas as pd\n\ndf = pd.DataFrame({'column1': [1, 2, 3, 4]})\ndata_sdk.upload_dataframe(df, 'Dataset Name')\n```\n\n```py\nimport geopandas as gpd\n\ngdf = gpd.read_file('path/to/data.geojson')\ndata_sdk.upload_dataframe(gdf, 'Dataset Name')\n```\n",
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

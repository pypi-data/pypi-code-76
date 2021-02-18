# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchling_api_client',
 'benchling_api_client.api',
 'benchling_api_client.api.aa_sequences',
 'benchling_api_client.api.assay_results',
 'benchling_api_client.api.assay_runs',
 'benchling_api_client.api.batches',
 'benchling_api_client.api.blobs',
 'benchling_api_client.api.boxes',
 'benchling_api_client.api.containers',
 'benchling_api_client.api.custom_entities',
 'benchling_api_client.api.dna_alignments',
 'benchling_api_client.api.dna_sequences',
 'benchling_api_client.api.dropdowns',
 'benchling_api_client.api.entries',
 'benchling_api_client.api.events',
 'benchling_api_client.api.exports',
 'benchling_api_client.api.folders',
 'benchling_api_client.api.inventory',
 'benchling_api_client.api.lab_automation',
 'benchling_api_client.api.label_templates',
 'benchling_api_client.api.locations',
 'benchling_api_client.api.oligos',
 'benchling_api_client.api.plates',
 'benchling_api_client.api.printers',
 'benchling_api_client.api.projects',
 'benchling_api_client.api.registry',
 'benchling_api_client.api.requests',
 'benchling_api_client.api.schemas',
 'benchling_api_client.api.tasks',
 'benchling_api_client.api.warehouse',
 'benchling_api_client.api.workflows',
 'benchling_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'httpx>=0.15.0,<0.16.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'benchling-api-client',
    'version': '0.12.2a0',
    'description': 'A client library for accessing Benchling API',
    'long_description': '# Benchling API Client\n\nA Python 3.6+ API Client for the [Benchling](https://www.benchling.com/) platform automatically generated from OpenAPI specs.\n\n*Important!* It is recommended to use the [Benchling SDK](https://pypi.org/project/benchling-sdk/) \ninstead of the API Client directly.',
    'author': 'Benchling Customer Engineering',
    'author_email': 'ce-team@benchling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

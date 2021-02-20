# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_serverless']
install_requires = \
['boto3>=1.9,<2.0', 'moto>=1.3,<2.0', 'pyyaml>=5.1,<6.0']

entry_points = \
{'pytest11': ['serverless = pytest_serverless']}

setup_kwargs = {
    'name': 'pytest-serverless',
    'version': '0.13.3',
    'description': 'Automatically mocks resources from serverless.yml in pytest using moto.',
    'long_description': 'pytest-serverless\n---\nAutomatically mocks resources defined in serverless.yml file using [moto](https://github.com/spulec/moto) and uses them in [pytest](https://github.com/pytest-dev/pytest).\n\nThis way you can focus on writing tests rather than defining enormous list of fixtures.\n\n| master | PyPI | Python | pytest | Licence |\n| --- | --- | --- | --- | --- |\n| ![Master](https://github.com/whisller/pytest-serverless/workflows/Master/badge.svg) | [![PyPI](https://img.shields.io/pypi/v/pytest-serverless.svg)](https://pypi.org/project/pytest-serverless/) | ![](https://img.shields.io/pypi/pyversions/pytest-serverless.svg) | `6.2` | ![](https://img.shields.io/pypi/l/pytest-serverless.svg) |\n\n## Pre installation requirements\n- `serverless` installed\n- `pytest` installed\n\n## Installation\n```sh\npip install pytest-serverless\n```\n\n## Usage\nAssuming your `serverless.yml` file looks like:\n```yaml\nservice: my-microservice\nresources:\n Resources:\n   TableA:\n     Type: \'AWS::DynamoDB::Table\'\n     DeletionPolicy: Delete\n     Properties:\n       TableName: ${self:service}.my-table\n       AttributeDefinitions:\n         - AttributeName: id\n           AttributeType: S\n         - AttributeName: company_id\n           AttributeType: S\n       KeySchema:\n         - AttributeName: id\n           KeyType: HASH\n       GlobalSecondaryIndexes:\n         - IndexName: company_id\n           KeySchema:\n             - AttributeName: company_id\n               KeyType: HASH\n           Projection:\n             ProjectionType: ALL\n           ProvisionedThroughput:\n             ReadCapacityUnits: 10\n             WriteCapacityUnits: 30\n       ProvisionedThroughput:\n         ReadCapacityUnits: 10\n         WriteCapacityUnits: 30\n```\n\nJust mark your test with `@pytest.mark.usefixtures("serverless")` and `pytest-serverless` will automatically create `my-microservice.my-table` dynamodb table.\n```python\nimport boto3\nimport pytest\n\n\n@pytest.mark.usefixtures("serverless")\ndef test():\n    table = boto3.resource("dynamodb").Table("my-microservice.my-table")\n    count_of_items = len(table.scan()["Items"])\n    assert count_of_items == 0\n```\n\n## Supported resources\n### AWS::DynamoDB::Table\n### AWS::SQS::Queue\n### AWS::SNS::Topic\n### AWS::S3::Bucket\n### AWS::KMS::Key\n',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whisller/pytest-serverless',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

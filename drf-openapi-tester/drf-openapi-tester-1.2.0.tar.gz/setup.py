# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_tester']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0',
 'djangorestframework',
 'inflection>=0.4.0,<0.5.0',
 'openapi-spec-validator>=0.2.9,<0.3.0',
 'prance>=0.16.0,<0.17.0',
 'pyYAML']

setup_kwargs = {
    'name': 'drf-openapi-tester',
    'version': '1.2.0',
    'description': 'Django test utility for validating OpenAPI response documentation',
    'long_description': '<a href="https://pypi.org/project/drf-openapi-tester/">\n    <img src="https://img.shields.io/pypi/v/drf-openapi-tester.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/snok/drf-openapi-tester">\n    <img src="https://codecov.io/gh/snok/drf-openapi-tester/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/drf-openapi-tester/">\n    <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="Supported Python versions">\n</a>\n<a href="https://pypi.python.org/pypi/drf-openapi-tester">\n    <img src="https://img.shields.io/badge/django%20versions-2.2%2B-blue" alt="Supported Django versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# DRF OpenAPI Tester\n\nDRF OpenAPI Tester is a test utility to validate API responses against OpenAPI 2 and 3 schema. It has built-in support\nfor:\n\n- OpenAPI 2/3 yaml or json schema files.\n- OpenAPI 2 schemas created with [drf-yasg](https://github.com/axnsan12/drf-yasg).\n- OpenAPI 3 schemas created with [drf-spectacular](https://github.com/tfranzel/drf-spectacular).\n\n## Installation\n\n```shell script\npip install drf-openapi-tester\n```\n\n## Usage\n\nFirst instantiate one or more instances of SchemaTester:\n\n```python\nfrom openapi_tester import SchemaTester\n\nschema_tester = SchemaTester()\n\n\n```\n\nIf you are using either [drf-yasg](https://github.com/axnsan12/drf-yasg)\nor [drf-spectacular](https://github.com/tfranzel/drf-spectacular) this will be auto-detected, and the schema will be\nloaded by the SchemaTester automatically. If you are using schema files though, you will need to pass the file path to\nthe tester:\n\n```python\nfrom openapi_tester import SchemaTester\n\n# path should be a string\nschema_tester = SchemaTester(schema_file_path="./schemas/publishedSpecs.yaml")\n\n\n```\n\nOnce you instantiate a tester, you can use it to validate a DRF Response in a test:\n\n```python\nfrom openapi_tester.schema_tester import SchemaTester\n\n# you need to create at least one instance of SchemaTester.\n# you can pass kwargs to it\nschema_tester = SchemaTester()\n\n\ndef test_response_documentation(client):\n    response = client.get(\'api/v1/test/1\')\n    assert response.status_code == 200\n    schema_tester.validate_response(response=response)\n```\n\nIf you are using the Django testing framework, you can create a base APITestCase that incorporates schema validation:\n\n```python\nfrom openapi_tester.schema_tester import SchemaTester\nfrom rest_framework.test import APITestCase\nfrom rest_framework.response import Response\n\nschema_tester = SchemaTester()\n\n\nclass BaseAPITestCase(APITestCase):\n    """ Base test class for api views including schema validation """\n\n    @staticmethod\n    def assertResponse(response: Response, **kwargs) -> None:\n        """ helper to run validate_response and pass kwargs to it """\n        schema_tester.validate_response(response=response, **kwargs)\n```\n\nThen use it in a test file:\n\n```python\nfrom shared.testing import BaseAPITestCase\n\n\nclass MyAPITests(BaseAPITestCase):\n    def test_some_view(self):\n        response = self.client.get("...")\n        self.assertResponse(response)\n```\n\n## Options\n\nWe currently support the following optional kwargs:\n\n### Case tester\n\nThe case tester argument takes a callable to validate the case of both your response schemas and responses. If nothing\nis passed, case validation is skipped.\n\nThe library currently has 4 build-in functions that can be used:\n\n- `is_pascal_case`\n- `is_snake_case`\n- `is_camel_case`\n- `is_kebab-case`\n\nfor example:\n\n```python\nfrom openapi_tester import SchemaTester, is_camel_case\n\nschema_test_with_case_validation = SchemaTester(case_tester=is_camel_case)\n\n```\n\nor\n\n```python\nfrom openapi_tester import SchemaTester, is_camel_case\n\nschema_tester = SchemaTester()\n\n\ndef my_test(client):\n    response = client.get(\'api/v1/test/1\')\n    assert response.status_code == 200\n    schema_tester.validate_response(response=response, case_tester=is_camel_case)\n```\n\nYou of course pass your own custom validator function.\n\n### Ignore case\n\nList of keys to ignore. In some cases you might want to declare a global list of keys exempt from case testing.\n\nfor example:\n\n```python\nfrom openapi_tester import SchemaTester, is_camel_case\n\nschema_test_with_case_validation = SchemaTester(case_tester=is_camel_case, ignore_case=["IP"])\n\n```\n\n## Schema Validation\n\nWhen the SchemaTester loads a schema, it runs it through\n[OpenAPI Spec validator](https://github.com/p1c2u/openapi-spec-validator) which validates that the schema passes without\nspecification compliance issues. In case of issues the validator will raise an error.\n\n## Known Issues\n\n* We are using [prance](https://github.com/jfinkhaeuser/prance) as a schema resolver, and it has some issues with the\n  resolution of (very) complex OpenAPI 2.0 schemas. If you encounter\n  issues, [please document them here](https://github.com/snok/drf-openapi-tester/issues/205).\n\n## Contributing\n\nContributions are welcome. Please see the [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': "Na'aman Hirschfeld",
    'maintainer_email': 'nhirschfeld@gmail.com',
    'url': 'https://github.com/snok/drf-openapi-tester',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

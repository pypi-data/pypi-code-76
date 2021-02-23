# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bx_py_utils',
 'bx_py_utils.approve_workflow',
 'bx_py_utils.aws',
 'bx_py_utils.data_types',
 'bx_py_utils.data_types.gtin',
 'bx_py_utils.dbperf',
 'bx_py_utils.humanize',
 'bx_py_utils.models',
 'bx_py_utils.templatetags',
 'bx_py_utils.test_utils',
 'bx_py_utils.view_utils']

package_data = \
{'': ['*'],
 'bx_py_utils': ['locale/de/LC_MESSAGES/*', 'locale/en/LC_MESSAGES/*'],
 'bx_py_utils.approve_workflow': ['locale/de/LC_MESSAGES/*',
                                  'locale/en/LC_MESSAGES/*',
                                  'templates/approve_workflow/*']}

install_requires = \
['django', 'python-stdnum']

entry_points = \
{'console_scripts': ['publish = '
                     'bx_py_utils_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'bx-py-utils',
    'version': '26',
    'description': 'Various Python / Django utility functions',
    'long_description': '# Boxine - bx_py_utils\n\nVarious Python / Django utility functions\n\n\n## Quickstart\n\n```bash\npip install bx_py_utils\n```\n\n\n## Existing stuff\n\nHere only a simple list about existing utilities.\nPlease take a look into the sources and tests for deeper informations.\n\n\n### models utilities\n\n* `approve_workflow` - Base model/admin/form classes to implement a model with draft/approve versions workflow\n* `manipulate.create_or_update()` - Similar to django\'s `create_or_update()` with benefits\n* `timetracking.TimetrackingBaseModel()` - Base model with "create" and "last update" date time\n\n### data types\n\n* `data_types.gtin` - ModelField, FormField and validators for GTIN/UPC/EAN numbers, more info: [data_types/gtin/README.md](https://github.com/boxine/bx_py_utils/blob/master/bx_py_utils/data_types/gtin/README.md)\n\n### test utilities\n\n* `datetime.MockDatetimeGenerator()` - Mock django `timezone.now()` with generic time stamps\n* `datetime.parse_dt()` - Handy `datetime.strptime()` convert\n* `html_assertion.HtmlAssertionMixin` - Unittest mixin class with usefull assertments around Django test client tests\n* `model_clean_assert.CleanMock()` - Context manager to track if model `full_clean()` was called\n* `users` - Utilities around user/permission setup for tests\n* `time.MockTimeMonotonicGenerator()` - Mock `time.monotonic()` with generic time stamps\n* `AssertQueries()` - Context manager with different checks of made database queries\n* `assert_json_requests_mock()` - Check the requests history of `requests_mock.mock()`\n* `assert_equal()` - Compare objects with a nice ndiff\n\n### performance analysis\n\n* `dbperf.query_recorder.SQLQueryRecorder` - Context Manager that records SQL queries executed via the Django ORM\n\n### humanize\n\n* `humanize.time.human_timedelta()` - Converts a time duration into a friendly text representation. (`X ms`, `sec`, `minutes` etc.)\n* `templatetags.humanize_time.human_duration()` - Verbose time since template tag, e.g.: `<span title="Jan. 1, 2000, noon">2.0 seconds</span>`\n* `filename.filename2human_name()` - Convert filename to a capitalized name\n* `filename.clean_filename()` - Convert filename to ASCII only via slugify\n* `pformat()` - Better `pretty-print-format` using JSON with fallback to `pprint.pformat()`\n\n### view utilities\n\n* `view_utils.dynamic_menu_urls.DynamicViewMenu()` - Register views to build a simple menu with sections\n\n\n### AWS stuff\n\n* `bx_py_utils.aws.secret_manager.SecretsManager` - Get values from AWS Secrets Manager\n* `bx_py_utils.test_utils.mock_aws_secret_manager.SecretsManagerMock` - Mock our `SecretsManager()` helper in tests\n* `bx_py_utils.test_utils.mock_boto3session.MockedBoto3Session` - Mock `boto3.session.Session()` (Currently only `get_secret_value()`)\n* `bx_py_utils.aws.client_side_cert_manager.ClientSideCertManager` - Helper to manage client-side TLS certificate via AWS Secrets Manager\n\n\n### misc\n\n* `dict_utils.dict_get()` - nested dict `get()`\n* `dict_utils.pluck()` - Extract values from a dict, if they are present\n* `environ.cgroup_memory_usage()` - Get the memory usage of the current cgroup\n* `error_handling.print_exc_plus()` - Print traceback information with a listing of all the local variables in each frame\n* `iteration.chunk_iterable()` - Create chunks off of any iterable\n* `processify.processify()` - Will execute the decorated function in a separate process\n* `stacktrace.get_stacktrace()` - Returns a filterable and easy-to-process stacktrace\n* `anonymize.anonymize()` - Anonymize a string (With special handling of email addresses)\n* `hash_utils.url_safe_hash()` - Generate URL safe hashes\n\n\n## developing\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/bx_py_utils.git\n~$ cd bx_py_utils\n~/bx_py_utils$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\ntox-py36             Run pytest via tox with *python v3.6*\ntox-py37             Run pytest via tox with *python v3.7*\ntox-py38             Run pytest via tox with *python v3.8*\ntox-py39             Run pytest via tox with *python v3.9*\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nmakemessages         Make and compile locales message files\nstart-dev-server     Start Django dev. server with the test project\nclean                Remove created files from the test project (e.g.: SQlite, static files)\n```\n\nYou can start the test project with the Django developing server, e.g.:\n```bash\n~/bx_py_utils$ make start-dev-server\n```\nThis is a own manage command, that will create migrations files from our test app, migrate, collectstatic and create a super user if no user exists ;)\n\nIf you like to start from stretch, just delete related test project files with:\n```bash\n~/bx_py_utils$ make clean\n```\n...and start the test server again ;)\n\n\n## License\n\n[MIT](LICENSE). Patches welcome!\n\n## Links\n\n* https://pypi.org/project/bx-py-utils/\n',
    'author': 'Jens Diemer',
    'author_email': 'jens.diemer@boxine.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0.0',
}


setup(**setup_kwargs)

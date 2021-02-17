# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.logkit', 'outcome.logkit.fixtures']

package_data = \
{'': ['*']}

install_requires = \
['outcome-utils>=5.0.0,<6.0.0', 'structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'outcome-logkit',
    'version': '1.1.0',
    'description': 'Logging helpers.',
    'long_description': '# logkit-py\n![Continuous Integration](https://github.com/outcome-co/logkit-py/workflows/Continuous%20Integration/badge.svg) ![version-badge](https://img.shields.io/badge/version-1.1.0-brightgreen)\n\nLogging helpers.\n\n## Installation\n\n```sh\npoetry add outcome-logkit\n```\n\n## Usage\n\n`logkit` is a wrapper around [structlog](https://www.structlog.org/en/stable/) that configures it with the following:\n\n- Sets log level based on `APP_ENV` environment variable\n- Automatically outputs Stackdriver-compliant JSON to stdout when running in a GCP environment (AppEngine, CloudRun, GKE, etc.)\n- Intercepts all messages sent to the standard library loggers and processes them transparently\n- Configures structlog to provide async-safe context values\n\n### Initialization\n`logkit` needs to be initialized before being used. This initialization configures `structlog` and sets up the intercept for the standard logging library.\n\n**Note** It\'s important to do this as early as possible in the program to ensure that no other imports start logging messages before the intercept has been configured. You can use `# isort:skip` to ensure `isort` doesn\'t reorder the import.\n\n```py\n# Important that this happens before any other imports\nfrom outcome.logkit import init_logging  # isort:skip\n\ninit_logging()  # isort:skip\n```\n\n#### Log Level\nYou can provide a `level` parameter to `init_logging` to define the default log-level. You can use the built-in log levels from the `logging` module (e.g. `logging.INFO`). If you don\'t provide a level, it will automatically be set based on the `env.is_prod()` method from the [outcome-utils](https://github.com/outcome-co/utils-py/blob/master/src/outcome/utils/env.py) package.\n\n```py\nimport logging\n\ninit_logging(level=logging.INFO)\n```\n\n\n#### Custom Processors\nYou can provide an array of your own [structlog processors](https://www.structlog.org/en/stable/processors.html) to `init_logging`. They will be merged into the processors provided by `logkit`.\n\n```py\ninit_logging(processors=[my_custom_processor])\n```\n\n### Logging\nTo log with `logkit`, you can either use the standard library logging, or use the structlog interface. Both can be used to pass structured data to the log entries. Using the structlog interface is _marginally_ faster, since all the messages sent to the standard logging library are sent to structlog anyway.\n\n```py\nimport logging\nfrom outcome.logkit import get_logger\n\n# Using the standard library\nlogger = logging.getLogger(__name__)\nlogger.info(\'my_message\', user_id=\'1\')\n\n# Using the structlog interface\nstructured_logger = get_logger(__name__)\nstructured_logger.info(\'my_message\', user_id=\'1\')\n```\n\n#### Async-safe context vars\nYou can set "global" variables that are async safe using `outcome.logkit.context`.\n\n```py\nimport logging\nfrom outcome.logkit import get_logger, context\n\ncontext.add(user_id=\'1\')\n\nstructured_logger = get_logger(__name__)\nstructured_logger.info(\'my_message\')  # user_id=1 will be added to this log event\n\ncontext.remove(\'user_id\')\n```\n\n## Testing\n\nIf you want to capture logs during your tests, you can use `configure_structlog` and `log_output` fixtures.\n\n```py\n@pytest.mark.usefixtures(\'configure_structlog\')\ndef test_log_output(log_ouput):\n    assert log_output.entries == []\n    # do something\n    assert log_output.entries == [...]\n```\n\nYou can also define the captured `log level` or add `custom processors` thanks to these handy fixtures:\n\n```py\n@pytest.fixture\ndef log_level():\n    return logging.DEBUG\n\n\n@pytest.fixture\ndef log_processors(log_output):\n    my_custom_processor = foo\n    return [my_custom_processor, log_output]\n\n\n@pytest.mark.usefixtures(\'configure_structlog\')\ndef test_log_output(log_ouput):\n    assert log_output.entries == []\n    # do something\n    assert log_output.entries == [...]\n```\n\n## Development\n\nRemember to run `./bootstrap.sh` when you clone the repository.\n',
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/logkit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)

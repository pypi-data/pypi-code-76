# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ephios',
 'ephios.core',
 'ephios.core.forms',
 'ephios.core.migrations',
 'ephios.core.models',
 'ephios.core.signup',
 'ephios.core.templatetags',
 'ephios.core.views',
 'ephios.extra',
 'ephios.extra.management',
 'ephios.extra.management.commands',
 'ephios.extra.templatetags',
 'ephios.plugins',
 'ephios.plugins.basesignup',
 'ephios.plugins.basesignup.signup',
 'ephios.plugins.pages',
 'ephios.plugins.pages.migrations']

package_data = \
{'': ['*'],
 'ephios': ['locale/de/LC_MESSAGES/*',
            'static/bootstrap/css/*',
            'static/bootstrap/js/*',
            'static/clipboardjs/js/*',
            'static/ephios/css/*',
            'static/ephios/js/*',
            'static/ephios/js/formset/*',
            'static/fontawesome/css/*',
            'static/fontawesome/webfonts/*',
            'static/jquery/js/*',
            'static/plugins/basesignup/js/*',
            'static/select2/css/*',
            'static/select2/js/*',
            'static/select2/js/i18n/*',
            'static/sortablejs/*',
            'templates/*',
            'templates/registration/*'],
 'ephios.core': ['templates/core/*',
                 'templates/core/disposition/*',
                 'templates/core/fragments/*',
                 'templates/core/mails/*',
                 'templates/core/settings/*'],
 'ephios.plugins': ['basesignup/templates/basesignup/instant/*',
                    'basesignup/templates/basesignup/request_confirm/*',
                    'basesignup/templates/basesignup/section_based/*',
                    'pages/templates/pages/*']}

install_requires = \
['bleach>=3.2.1,<4.0.0',
 'django-bootstrap4>=2.2.0,<3.0.0',
 'django-compressor>=2.4,<3.0',
 'django-csp>=3.7,<4.0',
 'django-dynamic-preferences>=1.10.1,<2.0.0',
 'django-environ>=0.4.5,<0.5.0',
 'django-formset-js-improved>=0.5.0,<0.6.0',
 'django-guardian>=2.3.0,<3.0.0',
 'django-ical>=1.7.1,<2.0.0',
 'django-polymorphic>=3.0.0,<4.0.0',
 'django-select2>=7.4.2,<8.0.0',
 'django-statici18n>=2.0.1,<3.0.0',
 'django>=3.1,<4.0',
 'markdown>=3.2.2,<4.0.0',
 'reportlab>=3.5.51,<4.0.0']

extras_require = \
{'mysql': ['mysqlclient>=2.0.1,<3.0.0'], 'pgsql': ['psycopg2>=2.8.6,<3.0.0']}

setup_kwargs = {
    'name': 'ephios',
    'version': '0.3.1',
    'description': 'ephios is a tool to manage shifts for medical services.',
    'long_description': '![tests](https://github.com/ephios-dev/ephios/workflows/tests/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/ephios/badge/?version=latest)](https://docs.ephios.de/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/ephios)](https://pypi.org/project/ephios/)\n[![Coverage Status](https://coveralls.io/repos/github/ephios-dev/ephios/badge.svg?branch=main)](https://coveralls.io/github/ephios-dev/ephios?branch=main)\n[![translated by Weblate](https://hosted.weblate.org/widgets/ephios/-/svg-badge.svg)](https://hosted.weblate.org/engage/ephios/)\n\n\n# ephios\n\nephios is a tool to manage shifts for medical services.\nPlanners can create events for which volunteer help is required (e.g. security/medical services, beach patrols, exercises).\nAn event can contain multiple shifts for which different processes can be applied for signup \n(e.g. a direct confirmation for an event or an "application" that has to be accepted first).\nThe volunteers can register for the respective shifts via a clearly arranged web interface.\nThe planners can then assign personnel and have an overview of the current status.\nAround this central feature there are further supporting functions like the management of the volunteers and their\nqualifications or an overview of the volunteer hours worked. A flexible group systems helps to support complex permission\nszenarios. The functionality can be extended using plugins.\n\n## Documentation\nYou can find the documentation for ephios at [Read the Docs](https://docs.ephios.de/en/latest). This includes\nthe user guide and installation instructions.\n\n## Contributing\nContributions to ephios are very welcome. You can find information about contributing at our [Contribution page](https://docs.ephios.de/en/latest/development/contributing.html)\nWe are using Weblate for translations, you can also contribute [there](https://hosted.weblate.org/engage/ephios/).\n',
    'author': 'Julian Baumann',
    'author_email': 'julian@ephios.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ephios.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

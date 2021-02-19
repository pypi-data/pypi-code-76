# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fullctl',
 'fullctl.django',
 'fullctl.django.autocomplete',
 'fullctl.django.inet',
 'fullctl.django.management',
 'fullctl.django.management.commands',
 'fullctl.django.migrations',
 'fullctl.django.models',
 'fullctl.django.models.abstract',
 'fullctl.django.models.concrete',
 'fullctl.django.rest',
 'fullctl.django.rest.route',
 'fullctl.django.rest.serializers',
 'fullctl.django.rest.urls',
 'fullctl.django.rest.views',
 'fullctl.django.social',
 'fullctl.django.social.backends',
 'fullctl.django.social.pipelines',
 'fullctl.service_bridge']

package_data = \
{'': ['*'],
 'fullctl.django': ['static/common/*',
                    'static/common/20c/*',
                    'static/common/icons/*',
                    'static/common/icons/Indicator/Check-Ind/*',
                    'static/common/icons/Indicator/X-Ind/*',
                    'static/common/icons/icon/*',
                    'static/common/icons/ui-caret-caret/*',
                    'static/common/oauth/*',
                    'static/common/themes/*',
                    'templates/common/*',
                    'templates/common/apidocs/*',
                    'templates/common/app/*',
                    'templates/common/app/forms/*',
                    'templates/common/app/manage/*',
                    'templates/common/auth/*']}

install_requires = \
['Django>=2.2,<3',
 'celery>=5,<6',
 'django-autocomplete-light>=3,<=4',
 'django-grainy>=1.9.0,<2',
 'django-handleref>=0.5',
 'django-inet',
 'django-peeringdb',
 'django-reversion<4',
 'djangorestframework>=3.11,<4',
 'grainy>=1.6.0,<2',
 'peeringdb<2',
 'pip',
 'pyyaml',
 'social-auth-app-django<4']

entry_points = \
{'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'fullctl',
    'version': '0.1.0',
    'description': 'Core classes and functions for service applications',
    'long_description': None,
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fullctl/fullctl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

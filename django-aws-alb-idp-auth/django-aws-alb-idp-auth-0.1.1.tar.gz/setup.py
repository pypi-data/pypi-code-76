# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_aws_alb_idp_auth']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.6,<4.0.0', 'PyJWT[crypto]>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'django-aws-alb-idp-auth',
    'version': '0.1.1',
    'description': '',
    'long_description': '# djang-aws-alb-idp-auth\n![python test](https://github.com/opencollector/django-aws-alb-idp-auth/workflows/python%20test/badge.svg)\n## features\n\n- verify jwt\n- extract user claims\n\n## setup\n\n### middleware\n\nPut `django_aws_alb_idp_auth.middleware.alb_idp_auth_middleware` and `django.contrib.auth.middleware.RemoteUserMiddleware` after AuthenticationMiddleware.\n\n```\nMIDDLEWARE = [\n    ...\n    \'django.contrib.auth.middleware.AuthenticationMiddleware\',\n    \'django_aws_alb_idp_auth.middleware.alb_idp_auth_middleware\',\n    \'django.contrib.auth.middleware.RemoteUserMiddleware\',\n    ...\n]\n```\n\n## auth backend\nYou may use RemoteUserBackend as Authentication Backend to create accessing user model.\n\n```\nAUTHENTICATION_BACKENDS = [\n    \'django.contrib.auth.backends.RemoteUserBackend\',\n    # \'django_aws_alb_idp_auth.backends.CreateUsperUserBackend\',\n]\n```\n\n`django_aws_alb_idp_auth.backends.CreateUsperUserBackend` is very convenient RemoteUserBackend that creates superuser.\n\n## accessing user claims\n\nYou can get user claims from `request.META["django_aws_alb_idp_auth.middleware.user_claims"]`.\n',
    'author': 'Atsushi Odagiri',
    'author_email': 'aodagx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

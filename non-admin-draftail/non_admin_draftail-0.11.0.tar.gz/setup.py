# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['non_admin_draftail',
 'non_admin_draftail.templatetags',
 'non_admin_draftail.views']

package_data = \
{'': ['*'],
 'non_admin_draftail': ['static/non_admin_draftail/*',
                        'static_src/*',
                        'static_src/src/*',
                        'static_src/src/styles/*',
                        'templates/non_admin_draftail/_draftail_css.html',
                        'templates/non_admin_draftail/_draftail_css.html',
                        'templates/non_admin_draftail/_draftail_css.html',
                        'templates/non_admin_draftail/_draftail_css.html',
                        'templates/non_admin_draftail/_draftail_js.html',
                        'templates/non_admin_draftail/_draftail_js.html',
                        'templates/non_admin_draftail/_draftail_js.html',
                        'templates/non_admin_draftail/_draftail_js.html',
                        'templates/non_admin_draftail/document/*',
                        'templates/non_admin_draftail/draftail_media.html',
                        'templates/non_admin_draftail/draftail_media.html',
                        'templates/non_admin_draftail/draftail_media.html',
                        'templates/non_admin_draftail/draftail_media.html',
                        'templates/non_admin_draftail/embed/*',
                        'templates/non_admin_draftail/image/*',
                        'templates/non_admin_draftail/link/*',
                        'templates/non_admin_draftail/modal_base.html',
                        'templates/non_admin_draftail/modal_base.html',
                        'templates/non_admin_draftail/modal_base.html',
                        'templates/non_admin_draftail/modal_base.html',
                        'templates/non_admin_draftail/widgets/*']}

install_requires = \
['django>=2.2,<3.2', 'wagtail>=2.11,<2.13']

setup_kwargs = {
    'name': 'non-admin-draftail',
    'version': '0.11.0',
    'description': 'You can now use Wagtail Draftail editor on non-admin pages',
    'long_description': None,
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://timonweb.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

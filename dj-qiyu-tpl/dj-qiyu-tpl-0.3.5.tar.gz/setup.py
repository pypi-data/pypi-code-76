# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_qiyu_tpl',
 'dj_qiyu_tpl.fields',
 'dj_qiyu_tpl.forms',
 'dj_qiyu_tpl.migrations',
 'dj_qiyu_tpl.rst',
 'dj_qiyu_tpl.templatetags']

package_data = \
{'': ['*'],
 'dj_qiyu_tpl': ['static/dj_qiyu_tpl/img/*',
                 'static/dj_qiyu_tpl/js/*',
                 'static/dj_qiyu_tpl/vendor/bulma/*',
                 'static/dj_qiyu_tpl/vendor/darkreader/*',
                 'static/dj_qiyu_tpl/vendor/fa/css/*',
                 'static/dj_qiyu_tpl/vendor/fa/fonts/*',
                 'static/dj_qiyu_tpl/vendor/remixicon/*',
                 'static/dj_qiyu_tpl/vendor/rst/*',
                 'templates/dj_qiyu_tpl/*',
                 'templates/dj_qiyu_tpl/css/*',
                 'templates/dj_qiyu_tpl/fields/*',
                 'templates/dj_qiyu_tpl/forms/*',
                 'templates/dj_qiyu_tpl/js/*']}

install_requires = \
['django>=3.1,<3.2', 'docutils>=0.16,<0.17', 'pygments>=2.8,<3.0']

setup_kwargs = {
    'name': 'dj-qiyu-tpl',
    'version': '0.3.5',
    'description': 'Template for internal use',
    'long_description': '# Django Template for Internal Use\n\n![PyPI - Version](https://img.shields.io/pypi/v/dj-qiyu-tpl)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dj-qiyu-tpl)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/dj-qiyu-tpl)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/dj-qiyu-tpl)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/dj-qiyu-tpl)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/dj-qiyu-tpl)\n\nWARNING:\n\n    this may be useless for you\n\n中文:\n\n    可能对您没有任何用处\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

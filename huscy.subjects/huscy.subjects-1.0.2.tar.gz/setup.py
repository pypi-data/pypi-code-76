from os import path
from setuptools import find_namespace_packages, setup

from huscy.subjects import __version__


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


extras_require = {
    'development': [
        'psycopg2-binary',
    ],
    'testing': [
        'tox',
        'watchdog==0.9',
    ]
}

install_requires = [
    'Django>=2.1,<3.2',  # cap to version 3.1 until issues in django-countries are fixed
    'djangorestframework>=3.10',
    'django-countries>=5',
    'django-phonenumber-field[phonenumberslite]>=2.3',
    'drf-nested-routers>=0.90',
    'python-dateutil>=2.7',
]


setup(
    name='huscy.subjects',
    version=__version__,
    license='AGPLv3+',

    description='Managing subjects in a human research context.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Alexander Tyapkov, Mathias Goldau, Stefan Bunde',
    author_email='tyapkov@gmail.com, goldau@cbs.mpg.de, stefanbunde+git@posteo.de',

    url='https://bitbucket.org/huscy/subjects',

    packages=find_namespace_packages(include=['huscy.*']),

    install_requires=install_requires,
    extras_require=extras_require,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
    ],
)

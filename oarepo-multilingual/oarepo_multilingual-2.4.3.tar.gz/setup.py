# -*- coding: utf-8 -*-
"""Setup module for flask multilingual."""
import os

from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.md').read()

install_requires = [
    'marshmallow',
    'flask',
    'pycountry'
]

tests_require = [
    'pytest-invenio[docs]==1.3.4',
    'oarepo-mapping-includes'
]

extras_require = {
    'tests': [
        *tests_require,
        'oarepo[tests]'
    ],
}

setup_requires = [
    'pytest-runner>=2.7',
]

g = {}
with open(os.path.join('oarepo_multilingual', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name="oarepo_multilingual",
    version=version,
    url="https://github.com/oarepo/oarepo-multilingual",
    license="MIT",
    author="Alzbeta Pokorna",
    author_email="alzbeta.pokorna@cesnet.cz",
    description="Multilingual support for OARepo",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=['oarepo_multilingual'],
    entry_points={
        'oarepo_mapping_handlers': [
            'multilingual=oarepo_multilingual.mapping.mapping_handler:handler'
        ],
        'invenio_jsonschemas.schemas': [
            'oarepo_multilingual = oarepo_multilingual.jsonschemas'
        ],
        'invenio_base.apps': [
            'oarepo_multilingual = oarepo_multilingual.ext:OARepoMultilingualExt'
        ],
        'invenio_base.api_apps': [
            'oarepo_multilingual = oarepo_multilingual.ext:OARepoMultilingualExt'
        ],
    },
    include_package_data=True,
    setup_requires=setup_requires,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
    ],
)

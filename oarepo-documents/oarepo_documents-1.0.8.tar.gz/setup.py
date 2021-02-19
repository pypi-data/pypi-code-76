# -*- coding: utf-8 -*-
"""Setup module for flask taxonomy."""
import os

from setuptools import setup

readme = open('README.md').read()
history = open('CHANGES.md').read()
OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '3.3.0')


install_requires = [
    #'oarepo-records-draft',
    #'oarepo-actions',
    #'oarepo-validate',
    # 'coverage',
    'oarepo-mapping-includes',
    'marshmallow',
    # 'oarepo-multilingual',
    'flask',
    'crossrefapi',
    'deepmerge',
    'langdetect'
]

tests_require = [
    'oarepo-records-draft',
    'oarepo-actions',
    'oarepo-validate',
    'coverage',
    'oarepo-multilingual',
    'oarepo-mapping-includes',
    'invenio-search',
    'crossrefapi',
    'deepmerge',
    'langdetect',
]

extras_require = {
    'tests': [
    'oarepo[tests]~={version}'.format(
            version=OAREPO_VERSION),
        *tests_require,
        ],
    'tests-es7': [
    'oarepo[tests-es7]~={version}'.format(
            version=OAREPO_VERSION),
        *tests_require,
        ],
}

setup_requires = [
    'pytest-runner>=2.7',
]

g = {}
with open(os.path.join('oarepo_documents', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name="oarepo_documents",
    version=version,
    url="https://github.com/oarepo/oarepo-dc",
    license="MIT",
    author="Alzbeta Pokorna",
    author_email="alzbeta.pokorna@cesnet.cz",
    description="OARepo rdm records data model",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=['oarepo_documents'],
    entry_points={
        'oarepo_mapping_includes':[
            'oarepo_documents = oarepo_documents.included_mappings'
        ],
        #'invenio_search.mappings': [
        #    'documents= oarepo_documents.mappings',
        #],
        # 'invenio_search.mappings': [
        #     'test_mapping = test_mapping.mappings'
        # ],
        'invenio_jsonschemas.schemas': [
            'oarepo_documents = oarepo_documents.jsonschemas',
        ],
        'invenio_base.apps': [
            #'document = oarepo_documents.DocumentRecordMixin',
            'oarepo_actions = oarepo_actions:Actions'
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

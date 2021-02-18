# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '1.0.1rc11'


setup(
    name='valer.sync',
    version=version,
    description="VALER SYNC",
    long_description=open("README.rst").read() + "\n" +
                     open("CHANGES.rst").read() + "\n" +
                     "\n\n" +
                     "Authors and maintainers\n" +
                     "-----------------------\n\n" +
                     "- Valerio Zhang (Valer Group LLC) <valerio.zhang@valer.us>",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope2",
    ],
    keywords='',
    author="Valer Group LLC",
    author_email="valerio.zhang@valer.us",
    url='https://github.com/valeriozhang/senaite.sync',
    license='GPLv3',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['senaite'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'valer.api==1.2.3rc10',
        'valer.jsonapi==1.2.3rc9',
        'requests',
        'plone.api',
        'souper',
    ],
    extras_require={
        'test': [
            'Products.PloneTestCase',
            'Products.SecureMailHost',
            'plone.app.testing',
            'robotsuite',
            'unittest2',
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)

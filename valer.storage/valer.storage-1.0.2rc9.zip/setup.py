# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.STORAGE
#
# Copyright 2019 by it's authors

from setuptools import setup, find_packages

version = "1.0.2rc9"

setup(
    name="valer.storage",
    version=version,
    description="Sample storage add-on for VALER LIMS",
    long_description=open("README.rst").read(),
    # long_description_content_type="text/markdown",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords=['senaite', 'lims', 'opensource', 'valer'],
    author="Valer Group LLC",
    author_email="valerio.zhang@valer.us",
    url="https://github.com/valeriozhang/senaite.storage",
    license="GPLv2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "valer.lims==1.3.4rc9",
        "archetypes.schemaextender",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "Products.SecureMailHost",
            "plone.app.testing",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)

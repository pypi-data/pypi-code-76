# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "1.2.3rc10"

with open("docs/About.rst", "r") as fh:
    long_description = fh.read()

with open("src/senaite/api/docs/API.rst", "r") as fh:
    long_description += "\n\n"
    long_description += fh.read()

with open("src/senaite/api/docs/API_analysis.rst", "r") as fh:
    long_description += "\n\n"
    long_description += fh.read()

with open("docs/Changelog.rst", "r") as fh:
    long_description += "\n\n"
    long_description += "Changelog\n"
    long_description += "=========\n"
    long_description += fh.read()

setup(
    name="valer.api",
    version=version,
    description="VALER API",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope2",
    ],
    keywords="",
    author="Valer Group LLC",
    author_email="valerio.zhang@valer.us",
    url="https://github.com/valeriozhang/senaite.api",
    license="GPLv2",
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "plone.api",
        "valer.core==1.3.5rc9",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "Products.SecureMailHost",
            "plone.app.robotframework",
            "plone.app.testing",
            "robotframework-debuglibrary",
            "robotframework-selenium2library",
            "robotsuite",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)

import ast
import re
import sys
from os import getenv, path

from setuptools import find_packages, setup
from setuptools.command.install import install

_version_re = re.compile(r"__version__\s*=\s*(.*)")

with open("dbcat/__init__.py", "rb") as f:
    __version__ = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = getenv("CIRCLE_TAG")

        if tag != ("v%s" % __version__):
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, __version__
            )
            sys.exit(info)


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dbcat",
    version=__version__,
    packages=find_packages(exclude=["docs", "test*"]),
    url="https://tokern.io/data-dictionary",
    license="MIT",
    author="Tokern",
    author_email="info@tokern.io",
    description="Open Source Data Catalog For Snowflake, BigQuery, AWS Redshift and AWS Glue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/tokern/dbcat/tarball/" + __version__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="data-catalog databases postgres snowflake redshift glue",
    install_requires=[
        "click",
        "pyyaml",
        "jinja2",
        "amundsen-databuilder",
        "psycopg2-binary",
        "sqlalchemy",
        "google-api-python-client",
        "boto3",
        "pymysql",
        "cryptography>=3.3.2",
        "snowflake-sqlalchemy",
        "sqlalchemy",
    ],
    extra_requires=[],
    dependency_links=[],
    cmdclass={"verify": VerifyVersionCommand},
    entry_points={"console_scripts": ["dbcat = dbcat.__main__:main"]},
    include_package_data=True,
)

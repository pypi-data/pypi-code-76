from setuptools import find_packages, setup
import madeira_tools

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='madeira-tools',
    version=madeira_tools.__version__,
    description='Madeira Tools',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mxmader/madeira-tools",
    author='Joe Mader',
    author_email='jmader@jmader.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    package_data={
      'madeira_tools': ['cf_templates/*']
    },
    install_requires=[
        'boto3',
        'docopt',
        'madeira',
        'madeira-utils',
        'requests'
    ],
    scripts=[
        'bin/madeira-build-api',
        'bin/madeira-build-ui',
        'bin/madeira-deploy',
        'bin/madeira-clean-layers',
        'bin/madeira-package-layer',
        'bin/madeira-remove',
        'bin/madeira-run-api',
        'bin/madeira-run-dev',
        'bin/madeira-run-ui',
    ]
)

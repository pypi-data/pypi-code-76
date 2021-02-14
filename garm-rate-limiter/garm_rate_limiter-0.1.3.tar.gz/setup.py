#!/usr/bin/env python
"""The setup script."""
import sys

from setuptools import find_packages, setup


def get_version(filename):
    """Extract the package version"""
    with open(filename, encoding='utf8') as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.md', encoding='utf8') as readme_file:
    README = readme_file.read()

try:
    with open('HISTORY.md', encoding='utf8') as history_file:
        HISTORY = history_file.read()
except OSError:
    HISTORY = ''

# requirements for use
requirements = [
    'redis==3.5.*',
]

# requirements for development (testing, generating docs)
dev_requirements = [
    'better-apidoc',
    'coverage',
    'coveralls',
    'doctr-versions-menu',
    'flake8',
    'gitpython',
    'isort',
    'ipython',
    'pre-commit',
    'pdbpp',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'm2r',
    'recommonmark',
    'sphinx',
    'sphinx-autobuild',
    'sphinx-copybutton',
    'sphinx-autodoc-typehints',
    'sphinx_rtd_theme',
    'twine',
    'Werkzeug==1.0.*',
    'wheel',
]
if sys.version_info >= (3, 6):
    dev_requirements.append('black')

VERSION = get_version('./src/garm_rate_limiter/__init__.py')

setup(
    author="Burak Özdemir",
    author_email='burakozdemir32@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English',
    ],
    description=(
        "Rate Limiter for Flask"
    ),
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    license="MIT license",
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='garm_rate_limiter',
    name='garm_rate_limiter',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/burakozdemir32/garm_rate_limiter',
    version=VERSION,
    zip_safe=False,
)

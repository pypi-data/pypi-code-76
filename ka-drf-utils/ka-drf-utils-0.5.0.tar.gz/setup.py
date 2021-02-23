import codecs
import os
import re

from setuptools import setup, find_packages


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='ka-drf-utils',
    version=find_version('kitchenart', '__init__.py'),
    license='MIT',
    author='MSJ Development Team',
    author_email='engineering@muliasuksesjaya.com',
    description='KitchenArt utility package',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'gdn-python-common[drf]>=0.8.9',
    ],
    extras_require={
        'broker': [
            'kombu>=5.0',
            'msgpack==1.0.0',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

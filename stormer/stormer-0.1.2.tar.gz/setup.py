import os

from setuptools import find_packages, setup

import stormer

with open(os.path.join(os.path.dirname(__file__), 'README.md'), "r", encoding='utf-8') as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = (
    'this is a requester for requests.'
)

CLASSIFIERS = [
    'Programming Language :: Python',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
]
KEYWORDS = [
    'stormer', 'requester', 'redis', 'requests'
]

setup(
    name='stormer',
    version=stormer.__version__,
    maintainer='Murray',
    maintainer_email='sunglowrise@qq.com',
    url='https://github.com/sunglowrise/stormer/',
    download_url='https://github.com/sunglowrise/stormer/',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    platforms='Platform Independent',
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=[
        'requests>=2.22.0',
        'redis>=3.3.11',
        'redis-py-cluster>=2.1.0'
    ],
)

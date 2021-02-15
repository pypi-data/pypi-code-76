# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

tests_require = [
    'pytest==5.2.2',
    'pytest-aiohttp==0.3.0',
    'nose',
    'coverage',
    'flake8',
]

setup(
    name='aiohttp-prometheus-swaggered',
    version='0.1.2',
    description="HTTP metrics for a aiohttp application",
    long_description=open('README.rst').read(),
    keywords=['prometheus', 'aiohttp'],
    author='Globo.com, Rail Yakup',
    author_email='backstage@corp.globo.com, Rail1996@mail.ru',
    url='https://github.com/SirEdvin/aiohttp-prometheus.git',
    download_url='https://github.com/SirEdvin/aiohttp-prometheus/archive/0.1.1.tar.gz',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(
        exclude=(
            'tests',
        ),
    ),
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'prometheus-client',
    ],
    extras_require={
        'tests': tests_require,
    },
)

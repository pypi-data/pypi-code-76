from setuptools import setup
from dapeng import VERSION

setup(
    name='dapeng_cli',
    version=VERSION,
    license="MIT License",
    description="Command line tool for Dapeng system",
    packages=[
        'dapeng',
    ],
    entry_points={
        'console_scripts': [
            'dpc=dapeng.dpc:main',
            'dapeng=dapeng.dapeng:main'
            ],
    },
    install_requires=[
        "pika>=1.1.0",
        "requests",
        "click",
        "junit_xml"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
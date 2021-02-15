import setuptools
import awssh.awssh as awssh

VERSION = awssh.VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssh-aws',
    version=VERSION,
    description='SSH into your EC2 instances.',
    author='Francisco Duran',
    author_email='franciscogd@gatech.edu',
    url='https://gitlab.com/franciscogd/awssh',
    download_url='https://gitlab.com/franciscogd/awssh/archive/{}.tar.gz'.format(VERSION),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'awscli>=1.10.14',
        'boto3>=1.3.1'
    ],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    #  https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={
        # 'scripts': ['awssh = bin/awssh.sh'],
        'console_scripts': ['awssh = awssh.awssh:main'],
    }
)

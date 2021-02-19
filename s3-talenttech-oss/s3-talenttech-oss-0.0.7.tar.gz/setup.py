import os

from setuptools import setup, Command, find_packages


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./.pytest_cache ./.eggs')


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='s3-talenttech-oss',
    packages=find_packages(),
    version='0.0.7',
    license='MIT',
    description='TopMind S3 Helper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Pavel Popov',
    author_email='p.popov@talenttech.ru',
    url='https://github.com/severgroup-tt/topmind-commons',
    install_requires=[
        'boto3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    cmdclass={
        'clean': CleanCommand
    }
)

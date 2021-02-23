import json
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('package.json', 'r') as fh:
    package = json.loads(fh.read())

setup(
    name=package['name'],
    version=package['version'],
    author=package['author'],
    author_email='match@twilio.com',
    description=package['description'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=package['homepage'],
    packages=find_packages(exclude=['src']),
    classifiers=[
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)


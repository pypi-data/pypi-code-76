from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='CKMobile',
    version='0.0.1b1',
    description='ChokChaisak',
    long_description=readme(),
    url='https://github.com/ChokChaisak/ChokChaisak',
    author='ChokChaisak',
    author_email='ChokChaisak@gmail.com',
    license='ChokChaisak',
    install_requires=[
        'matplotlib',
        'numpy',
        'robotframework-appiumlibrary',
    ],
    keywords='CKMobile',
    packages=['CKMobile'],
    package_dir={
    'CKMobile': 'src/CKMobile',
    },
    package_data={
    'CKMobile': ['*'],
    },
)
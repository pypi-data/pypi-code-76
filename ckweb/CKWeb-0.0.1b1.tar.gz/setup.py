from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='CKWeb',
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
        'robotframework-seleniumlibrary'
    ],
    keywords='CKWeb',
    packages=['CKWeb'],
    package_dir={
    'CKWeb': 'src/CKWeb',
    },
    package_data={
    'CKWeb': ['*'],
    },
)
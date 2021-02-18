from setuptools import setup, find_packages

description = """\
MongoODM is a simple wrapper around pymongo or mongomock which allows for limited
class-based interactions with a Mongo Database.
"""


setup(
    name='mongoodm',
    long_description=description,
    long_description_content_type="text/x-rst",
    version='0.0.13',
    url='https://gitlab.com/opentrustee/mongoodm.git',
    author='Daniel Holmes',
    author_email='dan@centricwebestate.com',
    license='Commercial',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='object document mapper mongodb mongo',
    install_requires=['pymongo'],
    tests_require=[
        'mongomock',
        'simplejson'
    ],
    test_suite="tests",
    extras_require={
        'dev': [],
        'test': ['mongomock', 'simplejson'],
        'flaskapp': ['Flask'],

    }
)

'''
Flask-Zato
-------------

A simple Flask - Zato.io integration
'''
from setuptools import setup


setup(
    name='Flask-Zato',
    version='1.1.2',
    license='BSD',
    author='Michał Węgrzynek',
    author_email='mwegrzynek@litexservice.pl',
    description='Simple Zato integration for Flask',
    long_description=__doc__,
    py_modules=['flask_zato'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
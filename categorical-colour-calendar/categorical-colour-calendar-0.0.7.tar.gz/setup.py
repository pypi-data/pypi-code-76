from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='categorical-colour-calendar',
    version='0.0.7',
    description='Library for drawing monthly calendars and highlighting dates from categorical data',
    packages=[''],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erichards97/categorical-colour-calendar',
    author='Edward Richards',
    author_email='',
    install_requires=[
        'pandas>=1.2.1',
        'matplotlib>=3.3.4'
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.2',
            'check-manifest>=0.46',
            'twine>=3.3.0',
            'wheel>=0.36.2'
        ],
        'docs': [
            'sphinx==3.4.3'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
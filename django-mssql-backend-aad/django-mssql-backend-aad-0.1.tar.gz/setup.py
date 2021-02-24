from setuptools import find_packages, setup

CLASSIFIERS = [
    'License :: OSI Approved :: BSD License',
    'Framework :: Django',
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.0',
]

setup(
    name='django-mssql-backend-aad',
    version='0.1',
    description='Django backend for Microsoft SQL Server with AAD suport',
    long_description=open('README.rst').read(),
    author='Agustin Lucchetti',
    author_email='agustin.lucchetti@patagonian.it',
    url='https://bitbucket.org/patagoniantech/django-mssql-backend-aad',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'pyodbc>=3.0',
        'msal>=1.5.1'
    ],
    package_data={'sql_server.pyodbc': ['regex_clr.dll']},
    classifiers=CLASSIFIERS,
    keywords='django',
)

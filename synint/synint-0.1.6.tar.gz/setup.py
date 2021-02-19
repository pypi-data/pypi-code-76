from setuptools import setup

setup(
    name='synint',
    version='0.1.6',
    license='All Rights Reserved.',
    description='synint package',
    py_modules=["synint"],
    install_requires=[
          'numpy',
          'pandas'
      ],
    author = 'Aaron S. Parker',
    author_email = 'aparker@hitachisolutions.com',
    package_dir={'':'src'}
)
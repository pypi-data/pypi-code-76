from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='postgres_table_as_queue_tools',
    url='https://github.com/vinger4/pg_table_as_queue_tools',
    author='Evgenii Kozhanov',
    author_email='evgenii.kozhanov@gmail.com',
    packages=['pg_table_as_queue_tools'],
    install_requires=[],
    version='0.0.2',
    license='MIT',
    description='There are just only several function to getting SQL queries for manage your table as a queue.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)

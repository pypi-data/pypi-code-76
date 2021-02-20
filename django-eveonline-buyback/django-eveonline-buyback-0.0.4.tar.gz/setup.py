
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-eveonline-buyback',
    version=__import__('django_eveonline_buyback').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django extension providing an easy way to appraise buyback items in bulk.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/b5n/django-eveonline-buyback',
    author='Princep Machinor',
    author_email='princep@1337h4x0r420.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'wheel',
        'requests',
        'django-singleton-admin-2'
    ]
)

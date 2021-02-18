from distutils.core import setup
from revdb import __version__
from setuptools import find_packages

setup(
    name='revdb',
    version=__version__,
    license='MIT',
    description='database sdk for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    url='https://github.com/revtel/revdb',
    keywords=['revteltech', 'sdk'],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'mjango >= 0.2.0',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

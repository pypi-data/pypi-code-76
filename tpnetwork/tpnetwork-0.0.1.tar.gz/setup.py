#!/usr/bin/python3
import setuptools

long_description = '# python-network\nThis a python 3 network package'

setuptools.setup(
    name='tpnetwork',
    version='0.0.1',
    description='A python network package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomarrok/python-network',
    author='Thomas Pajon',
    author_email='th.pajon45@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix'
    ],
    keywords='python, networks, development',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/tomarrok/python-network#readme'
    }
)

from setuptools import setup, find_packages

setup(
    name='json_builder',
    packages=find_packages(),
    version='0.2',
    license='MIT',
    description='This module is built to provide straightforward way to build and modify json objects',
    author='Albert Dorcioman',
    author_email='albert.dorcioman@gmail.com',
    url='https://github.com/adorcioman/json_builder',
    download_url='https://github.com/adorcioman/json_builder/archive/v_0.2.tar.gz',
    keywords=['Json', 'Builder'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

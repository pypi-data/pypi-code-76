from distutils.core import setup
setup(
    name='fgdtools',
    packages=['fgdtools'],
    version='1.0.2',
    license='gpl-3.0',
    description='(DEPRECATED: check ValveFGD) A library to parse .fgd files used in the source engine.',
    author='Maxime Dupuis',
    author_email='mdupuis@hotmail.ca',
    url='https://maxdup.github.io/fgd-tools/',
    download_url='https://github.com/maxdup/fgd-tools/archive/v1.0.2.tar.gz',
    keywords=['fgd', 'source', 'sourcesdk', 'hammer', 'valve'],
    install_requires=['pyparsing', 'future'],
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

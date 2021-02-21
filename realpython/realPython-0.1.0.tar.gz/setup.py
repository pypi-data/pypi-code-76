from setuptools import setup

setup(
    name='realPython',
    version='0.1.0',
    description='This is a python package containing handy things like advanced and basic math calculations and translations.',
    url='https://github.com/coding610/realPython',
    author='Sixten Bohman',
    author_email='sixten.bohman.08@gmail.com',
    license='apache license 2.0',
    packages=['realPython'],
    install_requires=['translate'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
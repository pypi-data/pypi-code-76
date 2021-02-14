from setuptools import setup

version = __import__('yeast').__version__


setup(
    name='sgd-chromosomal-features',
    packages=['yeast'],
    version=version,
    long_description="Tools to work with Saccharomyces Cerevisiae chromosomal features from SGD",
    description="SGD Chromosomal Features tools",
    author='Matej Usaj',
    author_email='usajusaj@gmail.com',
    url='https://github.com/BooneAndrewsLab/sgd_chromosomal_features',
    license='MIT License',
    platforms=['any'],
    python_requires=">=3.6",
    install_requires=['intermine'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'collect_features=collect_features:main',
        ],
    }
)

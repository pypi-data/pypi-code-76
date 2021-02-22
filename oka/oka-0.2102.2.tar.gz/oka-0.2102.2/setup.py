from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
VERSION = "0.2102.2"
setup(
    name='oka',  # Required
    version=VERSION,  # Required
    description='Client for OKA repository',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/rabizao/oka',  # Optional
    author='Rafael A. Bizao, Davi P. dos Santos',  # Optional
    author_email='rabizao@gmail.com',  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='data, repository, archive, data science, machine learning',  # Optional
    packages=find_packages(where='oka'),  # Required
    python_requires='>=3.7, <4',

    install_requires=['requests', 'python-dotenv', 'tatu'],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/rabizao/oka/issues',
        'Source': 'https://github.com/rabizao/oka',
    },
)

package_dir = {'': 'oka'}  # For IDEs like Intellij to recognize the package.

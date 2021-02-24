
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='yeastarAPI',
    version='0.1.5',  # Required
    description='yeastar wireless terminal api client',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/Scobber/yeastarAPI',  # Optional
    author='The Scobber',  # Optional
    author_email='info@thescobber.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='api, networking, sms terminal',  # Optional

    #package_dir={'': 'yeastarapi'},  # Optional

    packages=find_packages(),  # Required

    python_requires='>=3.6, <4',

    #install_requires=['peppercorn'],  # Optional

    #extras_require={  # Optional
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    #entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Scobber/yeastarAPI/issues',
        'Say Thanks!': 'https://github.com/Scobber/yeastarAPI',
        'Source': 'https://github.com/Scobber/yeastarAPI/',
    },
)

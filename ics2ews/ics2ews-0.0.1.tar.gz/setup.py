from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ics2ews',
    description="Synchronize ICS to Exchange",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "ics2ews/version.py",
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wallento/ics2ews',
    author="Stefan Wallentowitz",
    author_email='stefan.wallentowitz@hm.edu',
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["ics2ews = ics2ews.sync:main"]},
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "ics",
        "requests",
        "exchangelib"
    ]
)

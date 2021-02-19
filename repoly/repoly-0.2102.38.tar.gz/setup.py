import setuptools

NAME = "repoly"

VERSION = "0.2102.38"

AUTHOR = 'Davi Pereira-Santos'

AUTHOR_EMAIL = 'dpsabc@gmail.com'

DESCRIPTION = 'Rectilinear polygons'

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

LICENSE = 'GPL3'

URL = 'https://github.com/davips/repoly'

DOWNLOAD_URL = 'https://github.com/davips/repoly/releases'

CLASSIFIERS = ['Intended Audience :: Science/Research',
               'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
               'Natural Language :: English',
               'Programming Language :: Python',
               'Topic :: Scientific/Engineering',
               # posix               'Operating System :: Linux',
               'Programming Language :: Python :: 3.7']

INSTALL_REQUIRES = [
    # 'matplotlib', 'plotly', 'numpy'
    'pyside6', 'python-dotenv', 'requests'
]

EXTRAS_REQUIRE = {
}

SETUP_REQUIRES = ['wheel']

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    packages=setuptools.find_packages(),
    setup_requires=SETUP_REQUIRES,
    url=URL,
    entry_points = {
        "console_scripts": [
            "repoly = repoly.app.main:run",
        ]
    }    # scripts=['main.py']
)

package_dir = {'': 'repoly'}  # So IDE (e.g. Intellij) can recognize the working dir when running with ctrl+shift+F10.

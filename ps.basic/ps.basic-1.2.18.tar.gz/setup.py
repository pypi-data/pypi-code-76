"""Setup."""

from setuptools import setup


version = "1.2.18"

INSTALL_REQUIRES = ["docopt", "pygraphviz"]

setup(
    name="ps.basic",
    version=version,
    description="Basic class used in PS environment",
    long_description=open("README.rst").read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords="PS",
    author="Setz",
    author_email="thomas@setz.de",
    url="https://bitbucket.org/drsetz/ps.basic",
    license='"License :: OSI Approved :: GNU General Public License (GPL)', 
    packages=["ps.basic"],
    package_dir={"": "src"},
    # include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "ps_shell_log=ps.basic.ps_shell_log:main",
        ],
    },
)

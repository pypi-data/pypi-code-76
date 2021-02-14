from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "gozer_engine",
    version = "0.1.4",
    author = "schism",
    author_email = "schism@schism15.com",
    description = "Browser engine for Gopher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "GPL v2",
    keywords = "gopher browser engine",
    url = "https://gitlab.com/schism15/gozer-engine",
    packages=find_packages('src', 'src.gozer_engine'),
    package_dir = {'': 'src'},
    install_requires = ['lark-parser'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.8',
)
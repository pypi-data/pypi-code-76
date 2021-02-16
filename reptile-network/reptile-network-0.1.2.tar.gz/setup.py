import setuptools
from reptile.constants import *

with open("README.package.md", "r") as fh:
    long_description = fh.read()
    long_description = long_description.replace('<package_name>', PACKAGE_NAME)
    long_description = long_description.replace('<package_version>', VERSION)

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/", У нас пока закрытая репа
    packages=setuptools.find_packages(
        exclude=EXCLUDES
    ),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

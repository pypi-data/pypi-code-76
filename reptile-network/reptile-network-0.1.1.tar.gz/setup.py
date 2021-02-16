import setuptools
from reptile.constants import *

with open("README.package.md", "r") as fh:
    description = fh.read()
    description = description.replace('<package_name>', PACKAGE_NAME)
    description = description.replace('<package_version>', VERSION)
    short_description, long_description = description.split('===')

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/", У нас пока закрытая репа
    packages=setuptools.find_packages(
        exclude=[
            '__tests__',
            'tests.py'
        ]
    ),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

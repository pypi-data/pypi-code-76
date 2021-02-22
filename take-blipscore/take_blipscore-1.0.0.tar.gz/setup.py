from setuptools import find_packages, setup
from take_blipscore import __author__ as author
from take_blipscore import __version__ as version

short_description = "Generate Blip Score metric."
long_description = open("README.md").read()

install_requires = [
    req
    for req in [
        line.split("#", 1)[0].strip()
        for line in open("requirements.txt", "r", encoding="utf-8")
    ]
    if req and not req.startswith("--")
]
classifiers = [
    "Programming Language :: Python :: 3.7",
    "Operating System :: OS Independent",
]

setup(
    name="take_blipscore",
    keywords=["BLiP", "score", "metrics"],
    version=version,
    author=author,
    author_email='anaytics.ped@take.net',
    maintainer='Take - D&A',
    maintainer_email='anaytics.ped@take.net',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    classifiers=classifiers,
    license="MIT License",
    python_requires='>=3.7'
)

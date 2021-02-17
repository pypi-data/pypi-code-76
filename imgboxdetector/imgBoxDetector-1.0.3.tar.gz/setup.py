import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="imgBoxDetector",
    version="1.0.3",
    description="A model to detect various objects in an image",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Anish Sofat",
    author_email="sofatanish16@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["imgBoxDetector","imgBoxDetector.data","imgBoxDetector.data.transforms","imgBoxDetector.analysis"],
    include_package_data=True,
    install_requires=["Pillow","numpy","matplotlib","torch","torchvision"],
)

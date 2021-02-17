import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="torch_package",
    version="1.0.0",
    description="A model to detect images",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Suryam Arnav Kalra",
    author_email="suryamkalra35@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["torch_package","torch_package.data","torch_package.data.transforms","torch_package.analysis"],
    include_package_data=True,
    install_requires=["scikit-learn","Pillow","numpy","matplotlib","jsonlines","torch","torchvision"],
)
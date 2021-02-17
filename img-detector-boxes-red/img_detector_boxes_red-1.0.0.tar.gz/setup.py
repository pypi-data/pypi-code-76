import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="img_detector_boxes_red",
    version="1.0.0",
    description="A model to detect images",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Satvik Bansal",
    author_email="satvik.bansal2001@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["img_detector_boxes_red","img_detector_boxes_red.data","img_detector_boxes_red.data.transforms","img_detector_boxes_red.analysis"],
    include_package_data=True,
    install_requires=["scikit-learn","Pillow","numpy","matplotlib","jsonlines","torch","torchvision"],
)

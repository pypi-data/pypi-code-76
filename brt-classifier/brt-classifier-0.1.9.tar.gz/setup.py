import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="brt-classifier",
    version="0.1.9",
    description="A command-line tool for automatically classifying binary and ternary labelling problems on bipartite rooted trees (hence BRT).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AleksTeresh/tree-classifications",
    author="Aleksandr Tereshchenko",
    author_email="aleksandr.tereshch@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["brt_classifier", "brt_classifier.postprocess"],
    data_files=[
        ('data',['brt_classifier/problems/2labels.json']),
        ('data',['brt_classifier/problems/3labels.json']),
    ],
    include_package_data=True,
)

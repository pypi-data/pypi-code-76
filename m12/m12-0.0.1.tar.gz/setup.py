import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="m12",
    version="0.0.1",
    description="Template",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/m12",
    author="microprediction",
    author_email="pcotton@intechinvestments.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["m12"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["wheel", "pathlib"],
    entry_points={
        "console_scripts": [
            "m12=m12.__main__:main",
        ]
    },
)

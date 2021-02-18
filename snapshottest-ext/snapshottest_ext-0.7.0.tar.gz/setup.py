import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="snapshottest_ext",
    version="0.7.0",
    description="extra formatter for snapshottest",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/swuecho/snapshottest_ext",
    author="Hao Wu",
    author_email="echowuaho@foxmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['snapshottest_ext'],
    include_package_data=True,
    install_requires=["snapshottest", "pandas"],
)

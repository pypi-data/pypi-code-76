from setuptools import setup, find_packages
import pathlib
VERSION = '0.1.7'
DESCRIPTION = 'Helps in general Mac address operations which includes changing the current mac address of a certain interface, generating a mac address, getting the current mac address and also resetting the current mac address to the original one'
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="macops",
    version="3.2.4",
    description="It is a python module which can help you to change the current mac address of a certain interface, generate a mac address, get the current mac address and also reset the current mac address to the original one.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ShounakKulkarni/MacOps/",
    author="Shounak Kulkarni",
    author_email="shounak_kulkarni@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages=["macops"],
    include_package_data=True,
    install_requires=["randmac"],
    entry_points={
        "console_scripts":[
            "macops_generate=macops.generate:generate_mac",
            "macops_change=macops.change:change_mac",
            "macops_get=macops.get:get_current_mac",
            "macops_reset=macops.reset:reset_original_mac"
        ]
    },
)
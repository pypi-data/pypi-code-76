from setuptools import setup

long_description = """
Simple progressbar function that prints an ASCII-based progressbar in the terminal with the additional textual description on the left and right-hand side. In programs where there is a long loop, this method can be used to print a progressbar with progress text.
"""

setup(
    name="py-progress",
    version="0.1",
    description="PyProgress: An ASCII-based progressbar",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/TheDementors/PyProgress",
    author="Abhishek Chatterjee",
    author_email="abhishek.chatterjee97@protonmail.com",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/TheDementors/PyProgress/issues",
        "Documentation": "https://github.com/TheDementors/PyProgress",
        "Source Code": "https://github.com/TheDementors/PyProgress",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=[
        "py_progress",
    ],
    include_package_data=True,
)
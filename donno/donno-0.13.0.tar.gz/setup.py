import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="donno",
    version="0.13.0",
    author="Li Chao",
    author_email="clouds@isrc.iscas.ac.cn",
    description="A simple note-taking CLI application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leetschau/donno",
    packages=setuptools.find_packages(),
    install_requires=[
        "sh >= 1.14.0",
        "fire >= 0.3.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="note pim",
    entry_points={
        "console_scripts": [
            "don = donno.app:main",
        ],
    }
)

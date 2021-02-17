import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TemporalBackbone",
    version="0.1.3",
    author="Matthieu Nadini",
    author_email="matthieu.nadini@gmail.com",
    description="A tool to detect the backbone in temporal networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matnado/TemporalBackbone",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
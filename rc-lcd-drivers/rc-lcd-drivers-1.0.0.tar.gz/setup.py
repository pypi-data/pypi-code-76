import setuptools
import rclcd_drivers as d

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name=d.LIB_NAME,
    version=d.LIB_VERSION,
    author=d.LIB_AUTHOR,
    license=d.LIB_LICENSE,
    description=d.LIB_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=d.LIB_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers"
    ],
    install_requires=[
        "raspi"
    ],
    extras_require={
        "dev": [
            "setuptools",
            "wheel",
            "pytest",
            "flake8",
            "twine",
            "sphinx",
            "sphinx_rtd_theme",
        ]
    },
    python_requires='>=3',
)

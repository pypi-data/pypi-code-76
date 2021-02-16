import os
import sys

import setuptools

version=sys.argv[-1]
sys.argv.remove(sys.argv[-1])

package_name=sys.argv[-1]
sys.argv.remove(sys.argv[-1])

with open(os.path.dirname(os.path.abspath(__file__)) + "/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=package_name,
    version=version,
    author="Dragos Raducanu",
    author_email="raducanudragos12@gmail.com",
    description="ALIS (Arch Linux Installer Script)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Inonut/alis",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    entry_points = {
        "console_scripts": ["alis = alis.__main__:console_entry_point"]
    }
)

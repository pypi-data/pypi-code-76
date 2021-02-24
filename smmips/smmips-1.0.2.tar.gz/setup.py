
from setuptools import setup, find_packages

# Utility function to read the README file.
with open("README.md") as infile:
    content = infile.read().rstrip()

setup(
	name = "smmips",
	version = '1.0.2',
	author = "Richard Jovelin",
	author_email = "richard.jovelin@oicr.on.ca",
	description = ("A package to analyse smMIP libraries"),
	license = "MIT License",
	keywords = "computational genomics",
	url = "https://github.com/oicr-gsi/pysmmips",
	packages=find_packages(),
    
    long_description = content,
	classifiers = [
	"Development Status :: 3 - Alpha",
	"Intended Audience :: Science/Research",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.6",
	"Topic :: Software Development",
	"Topic :: Scientific/Engineering",
	"Operating System :: POSIX",
	"Operating System :: Unix",
	"Operating System :: MacOS",
	],
    entry_points={'console_scripts': ['smmips = smmips.smmips:main']},
	install_requires = ["regex>=2020.6.8", "pysam>=0.14.1", "biopython>=1.78"],
    python_requires=">=3.6",
)

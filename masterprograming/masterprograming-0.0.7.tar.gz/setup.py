from setuptools import setup , find_packages

classifiers = [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Education",
	"Operating System :: Microsoft :: Windows :: Windows 10",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
	]

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name = "masterprograming",
	version="0.0.7",
	author = "Danish Ali",
	author_email = "help@masterprograming.com",
	description = "Master Programing is a PIP Package that enables people that aren’t well to Build Software By Coding And its provides already Build Software ",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "",
	packages= find_packages(),
	classifiers=classifiers,
	python_requires='>=3.6',
)	

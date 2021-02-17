from setuptools import setup, find_packages

with open("README.md", "rt") as f:
	long_desc = f.read()

setup(
	name="fetools",
	version="1.2.1",
	description="Makes some tasks easier for VATUSA FEs.",
	long_description=long_desc,
	long_description_content_type="text/markdown",
	url="https://github.com/cessnahat/fetools",
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3 :: Only",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Developers",
		"Natural Language :: English"
	],
	keywords="vatsim vrc vstars veram",
	packages=find_packages(),
	python_requires=">=3.6, <4"
)

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
	long_description = f.read()

setuptools.setup(
	name="google-utils",
	version="1.0.2",
	author="medjed",
	author_email="imoshugi01@gmail.com",
	description="A utility package to interact with google.com",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/medjedqt/google-utils",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities"
	],
	packages=setuptools.find_packages(),
	install_requires=[
		"bs4",
		"requests",
	],
	python_requires=">=3.6"
)
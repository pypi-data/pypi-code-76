import setuptools

version = "0.0.0"

setuptools.setup(
	name = "pybryt",
	version = version,
	author = "Chris Pyles",
	author_email = "cpyles@berkeley.edu",
	description = "Python auto-assessment library",
	# long_description = long_description,
	# long_description_content_type = "text/markdown",
	# url = '",
	license = "MIT",
	packages = setuptools.find_packages(exclude=["test"]),
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	],
	# install_requires=install_requires,
)

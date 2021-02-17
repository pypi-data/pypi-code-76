import setuptools

setuptools.setup(
	name="json_key_press",
	version="2.0",
	author="Hendrik Lankers",
	author_email="hendrik.lankers.hl@googlemail.com",
	description="Tool for compression and decompression of dictionary keys for json transfer over limited networks",
	long_description="""
# JSON Key Press

This project aims at minimizing the size of json when transferring data over the network
by compressing the keys of a dictionary.

A more detailed description can be found [on github](https://github.com/elsholz/json_key_press).
""",
	long_description_content_type="text/markdown",
	url="https://github.com/elsholz/json_key_press",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent"
	],
	python_requires=">=3.5"
)

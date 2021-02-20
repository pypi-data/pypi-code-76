import setuptools
import os

PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

with open(PATH + "README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="alfonslistener",
	version="0.0.1",
	author="Anton Lindroth",
	author_email="ntoonio@gmail.com",
	description="Package to run a script when a packet is published to a topic on Alfons",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ntoonio/AlfonsListener",
	packages=setuptools.find_packages(),
	install_requires=[
		"alfonsiot==0.0.11",
		"PyYAML==5.4.1"
	]
)

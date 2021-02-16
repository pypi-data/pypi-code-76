import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antibody-transformer",
	version="0.0.1",
	author="Nicholas Bhattacharya",
	description="Attention-based antibody models.",
	long_description=long_description,
	long_description_content_type="text/markdown",
)

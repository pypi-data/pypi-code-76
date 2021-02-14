import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cirRelArea", # Replace with your own username
    version="0.1",
    author="Sparsh Agarwal",
    author_email="faint.artist@gmail.com",
    description="A Mathematical Tool to solve questions related to arithmetic progressions ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)    
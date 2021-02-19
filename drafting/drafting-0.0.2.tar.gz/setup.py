import setuptools

long_description = """
# Drafting

Color and geometric primitives
"""

setuptools.setup(
    name="drafting",
    version="0.0.2",
    author="Rob Stenson / Goodhertz",
    author_email="rob@goodhertz.com",
    description="Color and geometric primitives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goodhertz/drafting",
    packages=[
        "drafting",
        "drafting.sh",
        "drafting.grid",
        "drafting.pens",
        "drafting.color",
        "drafting.geometry",
        "drafting.interpolation"
    ],
    install_requires=[
        "fontPens",
        "fonttools",
        "more-itertools",
        "skia-pathops",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

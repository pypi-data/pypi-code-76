import setuptools

long_description = """
# PrettyTextTestRunner
A rich drop-in replacement for unittest.TextTestRunner which simply works out of the box. This
light weight implementation uses class extension and method overrides to get things working, with no
additional (outside of default Python) libraries required.  Get started and get things done with
ease. See the [Github project page|https://github.com/villagertech/PyPrettyTextTestRunner] for more information.
"""

setuptools.setup(
    name="PrettyTextTestRunner", # Replace with your own username
    version="0.1.1",
    author="Rob MacKinnon",
    author_email="rome@villagertech.com",
    description="Rich drop-in replacement for unittest.TextTestRunner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/villagertech/PyPrettyTextTestRunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)

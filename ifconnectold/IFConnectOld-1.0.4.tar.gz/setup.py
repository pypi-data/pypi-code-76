import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IFConnectOld", # Replace with your own username
    version="1.0.4",
    author="Matthew Shen",
    author_email="flyme2bluemoon@wearehackerone.com",
    description="A module using python to connect to the Infinite Flight Connect API v1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flyme2bluemoon/InfiniteFlightConnect-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.0',
)

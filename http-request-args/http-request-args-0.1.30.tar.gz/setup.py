import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="http-request-args",
    version="0.1.30",
    author="Quaking Aspen",
    author_email="info@quakingaspen.net",
    license='MIT',
    description="This library is to validate the request body and query string arguments. "
                "This library is implemented to be used with flask-restplus library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quakingaspen-codehub/http-request-args",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platform=['Any'],
    python_requires='>=3.6',
)

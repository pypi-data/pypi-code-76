import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="http_request_response",
    version="0.0.18",
    author="Quaking Aspen",
    author_email="info@quakingaspen.net",
    license='MIT',
    description="The main target of this library is to standardize the request response in case of using flask-restplus library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quakingaspen-codehub/http_request_response",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platform=['Any'],
    python_requires='>=3.6',
    install_requires=['http-status-code']
)

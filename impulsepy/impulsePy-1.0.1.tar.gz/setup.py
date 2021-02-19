import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impulsePy", # Replace with your own username
    version="1.0.1",
    author="DENSsolutions",
    author_email="merijn.pen@DENSsolutions.com",
    description="Library for controlling Impulse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
          'zmq',
          'pandas',
          'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
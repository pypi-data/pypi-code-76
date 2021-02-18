import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sximage",
    version="0.0.2",
    author="StreamLogic, LLC",
    description="StreamLogic SxImage Python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["sximage"],
    entry_points={
        'console_scripts': [
            'fpgacap = sximage.fpgacap:fpgacap',
            ]
        },
    install_requires=['pyserial','numpy','opencv-python']
)

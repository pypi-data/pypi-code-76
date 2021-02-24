import setuptools

setuptools.setup(
    name="pywrapper-flask",
    version="0.1.0",
    author="Hernan Romer",
    author_email="nanug33@gmail.com",
    description="Package to auto marshall and unmarshall flask requests",
    url="https://github.com/hgromer/pywrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JWST_FOV_plotter",
    version="0.1.3",
    author="Pablo Arrabal Haro",
    author_email="parrabalh@gmail.com",
    description="Simple tools to easily represent JWST FOVs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/parrabalh/jwst_fov_plots",
    packages=setuptools.find_packages(),
    package_data={"": ['*.csv']},
    license='LICENSE',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)

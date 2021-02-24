import setuptools
with open("README.md") as r:
    readme=r.read()

for line in open("satiopst\__init__.py").read().splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            var=str(line.split(delim)[1])

setuptools.setup(
    name="SatIOpsT",
    version=var,
    author="GeoEspacioTech Pvt. Ltd., Subhadip Datta, Soumyadeep Dutta",
    author_email="geoespaciotech@gmail.com",
    description="Satellite Image Operations Toolbox",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/SubhadipDatta/SatIOpsT/wiki",
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "geopandas",
        "rasterio",
        "scipy",
        "pandas",
        "numpy",
    ],
    include_package_data=True,
)


import setuptools

with open("READMEpy.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GalletaPy",
    version="0.36",
    author="Juan Felipe Huan Lew Yee",
    author_email="felipe.lew.yee@gmail.com",
    description="Paquete con código para ERIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipelewyee/galleta",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={'': ['basis/*.bas']},
    include_package_data=True,    
    install_requires=['numpy','scipy','pubchempy'],
)


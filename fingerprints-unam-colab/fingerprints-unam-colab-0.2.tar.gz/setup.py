import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='fingerprints-unam-colab',  
     version='0.02',
     author="Arturo Curiel",
     author_email="me@arturocuriel.com",
     description="Extraction of fingerprint and palm data from grayscale images.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/forensics-colab-unam/fingerprints-unam-colab",
     packages=setuptools.find_packages(),
     install_requires=['numpy', 'scipy', 'matplotlib', 'opencv-python'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     #package_data={
     #    "fingerprints-unam-colab": ["resources/*"],
     #},
     entry_points = {
        'console_scripts': ['extract_fp=huellas.extract_fp:main'],
     },
 )

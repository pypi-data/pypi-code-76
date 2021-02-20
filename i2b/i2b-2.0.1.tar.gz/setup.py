import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='i2b',
    version='2.0.1',
    author='Sachin Chavan',
    author_email='sachinewx@gmail.com',
    description='Convert image into base64 string and store into the txt file',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='image base64 jpg png jpeg JPG JPEG TIF',
    url="https://github.com/sachinchavan9/image-encode-decode",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['i2b=img2b64.img2b64:main'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    ],
    python_requires='>=3.5',
    include_package_data=True,
    zip_safe=False
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Chaos Python Client", # Replace with your own username
    version="1.0.0",
    author="Arie Kurniawan",
    author_email="hubungi.aja@gmail.com",
    description="[Unofficial] Python client for contacting with chaos API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkwrn/chaos-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
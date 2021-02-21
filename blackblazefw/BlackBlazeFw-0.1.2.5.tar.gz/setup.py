import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BlackBlazeFw", # Replace with your own username
    version="0.1.2.5",
    author="Black Blaze",
    author_email="blckblze@gmail.com",
    description="A Minimalistic Web Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Black-Blaze/web-fw/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["gunicorn==20.0.4", "WebOb==1.8.6", "sniffio", "rfc3986", "hstspreload", "h11", "hpack", "hyperframe", "h2", "httpcore", "httpx", "googletrans"],
    python_requires='>=3.6',
)

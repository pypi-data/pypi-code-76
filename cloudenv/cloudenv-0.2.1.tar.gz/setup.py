import io
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}
with io.open('./src/cloudenv/version.py', encoding='utf-8') as f:
    exec(f.read(), meta)

setuptools.setup(
    name="cloudenv", # Replace with your own username
    version=meta['__version__'],
    author="Lucas Carlson",
    author_email="lucas@carlson.net",
    description="Keep Your Environmental Variables Secure And In Sync",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudenvhq/cloudenv-python/",
    packages=['cloudenv'],
    package_dir={'': 'src'},
    install_requires=['python-dotenv>=0.15.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description="BizAI Framework Package"

setuptools.setup(
    name="aw-bizai-framework",  # Replace with your own username
    version="0.0.7",
    author="Arun Wagle",
    author_email="arun.wagle@gmail.com",
    description="BizAI Framework Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL",
    packages=['framework'],
    package_data={
        'framework': ['*', '*/*', '*/*/*', '*/*/*/*'],
    },
    python_requires='>=3.6',
)

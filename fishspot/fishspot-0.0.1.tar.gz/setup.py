import setuptools

setuptools.setup(
    name="fishspot",
    version="0.0.1",
    author="Greg M. Fleishman",
    author_email="greg.nli10me@gmail.com",
    description="Tools for finding discrete bright spots in images",
    url="https://github.com/GFleishman/fishspot",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'scikit-image',
    ]
)

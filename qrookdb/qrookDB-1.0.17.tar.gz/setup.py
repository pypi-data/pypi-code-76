import setuptools

setuptools.setup(
    name="qrookDB",
    version="1.0.17",
    author="Kurush",
    author_email="kurush.kazakov@ya.ru",
    description="database connections package",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/qrook/db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

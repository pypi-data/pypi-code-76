import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guacamole-compose", # Replace with your own username
    version="0.0.1",
    author="John Burt",
    author_email="johnburt.jab@gmail.com",
    description="Easy deployment of Apache Guacamole.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphabet5/guacamole-compose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={'console_scripts': ['guacamole-compose = __init__:main']},
)
package_data = {
    'templates': ['*']
}
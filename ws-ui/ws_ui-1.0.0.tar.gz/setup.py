import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='ws_ui',
    version='1.0.0',
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='shell shortcut',
    install_requires=['tornado', 'prompt_toolkit'],
    long_description=long_description,
    packages=setuptools.find_packages(),
    scripts=['scripts/ws-ui'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

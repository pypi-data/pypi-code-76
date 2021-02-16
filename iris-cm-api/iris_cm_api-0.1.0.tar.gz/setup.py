import setuptools


try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except UnicodeDecodeError:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setuptools.setup(
    name="iris_cm_api",
    version="0.1.0",
    author="lordralinc",
    description="Iris CM API signals emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/lordralinc/iris_cm_api_emulator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "vkbottle @ git+https://github.com/timoniq/vkbottle@master",
        "tortoise-orm",
    ],
    include_package_data=True,
)

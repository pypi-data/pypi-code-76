import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='vade_api',
     version='0.8.5',
     scripts=['vade_api'],
     author="Christain Burke",

     author_email="christian@vadepark.com",
     description="An easy to use wrapper for vade realtime api",
     long_description=long_description,
     long_description_content_type="text/markdown",
     # url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     install_requires=["pytz", "tzwhere", "requests", "python-dateutil", "webcolors"],
     package_data={'': ['*.jpg']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )

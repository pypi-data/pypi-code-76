import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="Egfrd-Zixian-Fang",
  version="0.0.1",
  author="Zixian-Fang",
  author_email="f20091219@outlook.com",
  description="Easy to read and write password and name!",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/fangcatchina/egfrd/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
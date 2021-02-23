import setuptools

with open('README.rst', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(name='ysb_common',
                 version='1.5',
                 description='ysb common',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='ysb',
                 author_email='497257761@qq.com',
                 url='https://markdown.felinae.net',
                 keywords='django markdown editor editormd',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True,
                 classifiers=(
                     "Programming Language :: Python",
                     "Development Status :: 4 - Beta",
                     "Operating System :: OS Independent",
                     "License :: OSI Approved :: Apache Software License"
                 ),
                 install_requires=[
                     'oss2'
                 ]
                 )

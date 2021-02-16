from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.6'
]
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='m1key',
    version='0.3.0',
    description='A resume based package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Mithilesh Tiwari',
    author_email='shubhamtiwari.tiwari84@gmail.com',
    license='MIT',
    classifiers=classifiers,
    entry_points={
        "console_scripts": ["m1key=m1key.__main__:main"]
    },
    keywords='m1key',
    packages=find_packages(),
    include_package_data = True,
    install_requires=['opencv-python','requests','matplotlib','numpy','scikit-learn','Pillow','anytree']
)

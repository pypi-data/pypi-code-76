import setuptools

with open("readme.rst", "r") as fh:
    long_description = fh.read()

import os
name = 'cqh_util'
_dir = os.path.dirname(os.path.abspath(__file__))

init_path = os.path.join(_dir, name, '__init__.py')
print("init_path:{}".format(init_path))


def read_version():
    """
    Traceback (most recent call last):
    File "setup.py", line 22, in <module>
        version = read_version()
      File "setup.py", line 18, in read_version
        exec(code, d, d)
      File "<string>", line 3, in <module>
    KeyError: "'__name__' not in globals"
    知道了， 因为init_path里面有import
    """
    d = {}
    code = open(init_path).read()
    for line in code.splitlines():
        if line.startswith("__version__"):
            version =  line.split("=")[-1]
            return version.strip().strip('"').strip("'") # 渠道"0.1.1" 的引号
    raise ValueError("cannot find version")

version = read_version()
print("version:{}".format(version))

setuptools.setup(
    name=name,  # Replace with your own username
    version=version,
    author="chenqinghe",
    author_email="1832866299@qq.com",
    description="cqh utils function",
    long_description=long_description,
    long_description_content_type='',
    url="https://github.com/chen19901225/cqh_util",
    packages=setuptools.find_packages(),
    install_requires=[
        "gitpython", "jinja2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "cqh_file_watcher=cqh_file_watcher.run:main",
        ],
    },
    python_requires='>=3.6',
    include_package_data=True
)

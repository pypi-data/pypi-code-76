import console_tool,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass
try:
    long_desc=open("README.rst").read()
except OSError:long_desc=''

setup(
  name='console-tool',
  version=console_tool.__version__,
  description=console_tool.__doc__.replace('\n',''),
  long_description=long_desc,
  author=console_tool.__author__,
  author_email=console_tool.__email__,
  py_modules=['console_tool'], #这里是代码所在的文件名称
  keywords=["terminal","command-line","console","cmd"],
  classifiers=[
      'Environment :: Console',
      'Programming Language :: Python :: 3',
      "Topic :: Terminals"],
  install_requires=["colorama","termcolor"]
)

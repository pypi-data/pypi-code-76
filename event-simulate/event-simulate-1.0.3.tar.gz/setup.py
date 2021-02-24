import event,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc=event.__doc__.replace('\n','') + "Author: 七分诚意"
try:
    long_desc=event.__doc__+open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='event-simulate',
  version=event.__version__,
  description=desc,
  long_description=long_desc,
  author=event.__author__,
  author_email=event.__email__,
  url="https://pypi.org/project/event-simulate/",
  platform="win32",
  packages=['event'],
  keywords=["event","simulate","key","mouse","click","键盘","鼠标"],
  classifiers=[
      "Programming Language :: Python :: 3",
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Desktop Environment :: Window Managers :: Blackbox",
      "Topic :: Education"],
)

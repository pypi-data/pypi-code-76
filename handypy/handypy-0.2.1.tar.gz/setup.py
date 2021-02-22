from setuptools import setup

long_description = open("README.md").read()

setup(name='handypy',
      version='0.2.1',
      description='Handy Python scripts',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://jiayiliu.github.io/handypy/',
      author='Jiayi Liu',
      author_email='jiayiliu@users.noreply.github.com',
      license='MIT',
      packages=['handypy'],
      zip_safe=False)

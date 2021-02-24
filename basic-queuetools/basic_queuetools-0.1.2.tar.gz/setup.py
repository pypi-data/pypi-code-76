from setuptools import setup

setup(name='basic_queuetools',
      version='0.1.2',
      description='QueueTools are some special functions to help with software developing',
      url='http://gitlab.csn.uchile.cl/dpineda/queuetools',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPLv3',
      packages=['basic_queuetools'],
      install_requires=['networktools'],
      include_package_data=True,      
      package_dir={'basic_queuetools': 'basic_queuetools'},
      package_data={
          'basic_queuetools': ['../doc', '../docs', '../requeriments.txt', '../tests']},
      zip_safe=False)

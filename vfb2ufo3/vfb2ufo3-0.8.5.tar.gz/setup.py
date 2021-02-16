import setuptools

with open('README.md', 'rb') as f:
  readme = f.read().decode('utf_8')

setuptools.setup(
  name='vfb2ufo3',
  version='0.8.5',
  author='Jameson R. Spires',
  author_email='jameson.spires@gmail.com',
  description='UFO converter for Windows FontLab 5.2',
  url='https://github.com/spiratype/vfb_ufo3',
  license='MIT',
  packages=['vfb2ufo3'],
  long_description=readme,
  long_description_content_type='text/markdown',
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Other Environment',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    ],
  )

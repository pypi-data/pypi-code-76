from setuptools import setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements('requirements.txt')

with open('README.md') as f:
    long_description = f.read()

setup(name='keras_data_format_converter',
      packages=['keras_data_format_converter'],
      version="0.0.4rc3",
      description='Generates equal keras models with the desired data format',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/tensorleap/keras-data-format-converter',
      download_url='https://github.com/tensorleap/keras-data-format-converter/archive/v0.0.4rc3.tar.gz',
      author='Doron Har Noy',
      author_email='doron.harnoy@tensorleap.ai',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Image Recognition',
      ],
      keywords='machine-learning deep-learning keras neural-network tensorflow vgg resnet tensorleap',
      license='MIT',
      install_requires=reqs,
      zip_safe=False)

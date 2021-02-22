import setuptools

def read(fname):
    """ Return file content. """
    with open(fname) as f:
        content = f.read()

    return content

description = "A plug-n-play package to start using new relic APIs for data gathering"
try:
    long_description = read('README.MD')
except IOError:
    long_description = description

setuptools.setup(
    name="newrelic-api-parser",
    package=['newrelic-api-parser'],
    version="0.0.9",
    author="Bharat Sinha",
    author_email="bharat.sinha.2307@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bharat23/newrelic-api-parser",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords = ['new relic api', 'insights', 'new relic', 'apm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
    ],
    install_requires=[
          'requests',
      ],
    python_requires='>=3.6',
)

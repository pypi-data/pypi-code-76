import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-ext-utils",
    version="0.0.1",
    author="Andrei Koptev",
    author_email="akoptev1989@ya.ru",
    description="Useful utilities for your django project",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='django rest utils',
    url="https://github.com/a1k89/django-ext-utils",
    packages=setuptools.find_packages(exclude=["demo",]),
    install_requires=['Django>=2.0',
                      'Pillow',],
    extras_require={
        'with_rest': ['djangorestframework>=3.0'],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    include_package_data=True
)
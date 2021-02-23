import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-mixins-glib",
    version="0.0.1",
    author="Ajit Mourya",
    author_email="ajit@glib.ai",
    description="django mixins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GlibAI/django_mixins/",
    packages=setuptools.find_packages(exclude=['django_mixins', 'manage.py']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)

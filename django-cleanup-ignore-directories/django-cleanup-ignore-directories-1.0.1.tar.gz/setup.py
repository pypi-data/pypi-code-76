import setuptools

setuptools.setup(
    name='django-cleanup-ignore-directories',
    version='1.0.1',
    description='Extension of the django-cleanup project v4.0.0. Allows ignoring specified user directories',
    url='https://github.com/MausamGaurav/django_cleanup_ignore_directories',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django :: 2.2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
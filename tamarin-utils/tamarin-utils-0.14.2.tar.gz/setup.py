import setuptools

with open("tamarin/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tamarin-utils",
    version="0.14.2",
    author="Lamasoo team",
    author_email="tech@lamasoo.com",
    description="Lamasoo utils for developing web application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.lamasoo.com/crs-agency/tamarin",
    install_requires=[
        'requests',
        'djangorestframework',
        'elasticsearch[async]',
        'celery',
        'sentry-sdk',
        'python-dateutil',
        'firebase-admin',
        'google-api-python-client',
        'python-jose',
        'djangorestframework-simplejwt',
        'pycryptodome',
        'django-nose',
        'python-dateutil',
        'python-telegram-bot',
        'Pyrogram',
        'TgCrypto',
        'elastic-apm',
        'xlwt',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
)

# py setup.py sdist bdist_wheel
# twine upload dist/*

import setuptools
from mldock.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mldock",
    version=__version__,
    author="SheldonGrant",
    author_email="sheldz.shakes.williams@gmail.com",
    description="Global Machine learning helpers for docker based development. Build, train and deploy on cloud with docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SheldonGrant/locative-ml-global-helpers",
    packages=setuptools.find_packages(where='.'),
    package_data={
        'mldock': [
            'templates/sagemaker/tests/container_health/*.py',
            'templates/sagemaker/src/',
            'templates/sagemaker/src/*.py',
            'templates/sagemaker/src/utils',
            'templates/sagemaker/src/utils/*py',
            'templates/sagemaker/src/container',
            'templates/sagemaker/src/container/*.sh',
            'templates/sagemaker/src/container/Dockerfile',
            'templates/sagemaker/src/container/ __init__.py',
            'templates/sagemaker/src/container/training/__init__.py',
            'templates/sagemaker/src/container/training/train',
            'templates/sagemaker/src/container/prediction/*.py',
            'templates/sagemaker/src/container/prediction/serve',
            'templates/sagemaker/src/container/prediction/nginx.conf',
            'templates/sagemaker/service/compose/docker-compose.yml',
            'templates/sagemakerv2/src/',
            'templates/sagemakerv2/src/*.py',
            'templates/sagemakerv2/src/utils',
            'templates/sagemakerv2/src/utils/*py',
            'templates/sagemakerv2/src/container',
            'templates/sagemakerv2/src/container/*.sh',
            'templates/sagemakerv2/src/container/Dockerfile',
            'templates/sagemakerv2/src/container/ __init__.py',
            'templates/sagemakerv2/src/container/training/__init__.py',
            'templates/sagemakerv2/src/container/training/train',
            'templates/sagemakerv2/src/container/prediction/*.py',
            'templates/sagemakerv2/src/container/prediction/serve',
            'templates/sagemakerv2/src/container/prediction/nginx.conf',
            'templates/sagemakerv2/service/compose/docker-compose.yml',
            'templates/generic/tests/container_health/*.py',
            'templates/generic/service/compose/docker-compose.yml',
            'templates/generic/src/',
            'templates/generic/src/environment.py',
            'templates/generic/src/prediction.py',
            'templates/generic/src/trainer.py',
            'templates/generic/src/container',
            'templates/generic/src/container/*.sh',
            'templates/generic/src/container/Dockerfile',
            'templates/generic/src/container/ __init__.py',
            'templates/generic/src/container/training/',
            'templates/generic/src/container/training/train.py',
            'templates/generic/src/container/prediction/',
            'templates/generic/src/container/prediction/wsgi.py',
            'templates/generic/src/container/prediction/predictor.py',
            'templates/generic/src/container/prediction/nginx.conf'
        ]
    },
    setup_requires=['setuptools>=39.1.0', 'future'],
    extras_require={
        'ai-platform': ['google-cloud-storage', 'google-api-python-client'],
        'cli': ['click', 'docker', 'future', 'requests'],
        'sagemaker': ['boto3', 'sagemaker-training']
    },
    entry_points="""
        [console_scripts]
        mldock=mldock.__main__:cli
    """,
    keywords=["docker", "machine learning", "ml", "ml services", "MLaaS"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6"
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages
setup(
    name='nlp_nn',
    version='0.0.3.0',
    description='NLP NN Framework',
    long_description='NLP NN Framework',
    long_description_content_type="text/markdown",
    author='fubo',
    author_email='fb_linux@163.com',
    url='https://gitee.com/fubo_linux/nlp_nn',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "nlp_nn": [
            "third_models",
            "third_models/transformer.models",
            "third_models/transformer.models/albert_tiny_pytorch/*",
            "third_models/transformer.models/bert_model_pytorch/*",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'torch>=1.6',
        'fastapi>=0.55.1',
        'pydantic>=1.5.1',
        'tensorboard>=2.2.1',
        'transformers>=4.2.2',
        'jieba>=0.39',
        'typing'
    ],
    python_requires='>=3.6'
)

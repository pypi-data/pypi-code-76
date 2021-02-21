from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

UNITORCH_VERSION = "0.0.0.1"


def get_unitorch_version():
    return UNITORCH_VERSION


extras = {}

extras["gitpython"] = ["gitpython>=3.1.7"]
extras["editdistance"] = ["editdistance>=0.5.3"]

extensions = [
    CUDAExtension(
        "ngram_repeat_block_cuda",
        [
            "unitorch/clib/cuda/ngram_repeat_block_cuda.cpp",
            "unitorch/clib/cuda/ngram_repeat_block_cuda_kernel.cu",
        ],
    ),
]

install_requires = open('requirements.txt', 'r').read().split('\n')

setup(
    name="unitorch",
    version=get_unitorch_version(),
    author="fuliucansheng",
    author_email="fuliucansheng@gmail.com",
    description=
    "Unified training/inference framework based PyTorch for NLP / CV / REC / RL / GNN with SOTA and fast performance",
    long_description=open("readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="NLP NLG deep learning PyTorch",
    license="MIT",
    url="https://github.com/fuliucansheng/unitorch",
    packages=find_packages(
        where=".",
        exclude=["benchmarks", "tests", "competition", "__pycache__"]),
    include_package_data=True,
    setup_requires=[
        "cython",
        "numpy",
        "setuptools>=18.0",
    ],
    install_requires=install_requires,
    extras_require=extras,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    ext_modules=extensions,
    entry_points={
        "console_scripts": [
            "unitorch-auto-train = unitorch_cli.auto_train:cli_main",
            "unitorch-auto-infer = unitorch_cli.auto_infer:cli_main",
        ],
    },
    cmdclass={"build_ext": BuildExtension},
)

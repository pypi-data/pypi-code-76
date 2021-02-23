__version__ = '0.3.2'
git_version = 'bf5ce67e061aec5dd7d9a561a69963919ccffe77'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()

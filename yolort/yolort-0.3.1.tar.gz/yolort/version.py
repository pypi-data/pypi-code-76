__version__ = '0.3.1'
git_version = '2150b5a62a4e138f5b49a4df2e8b6cbfef2ec0fd'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()

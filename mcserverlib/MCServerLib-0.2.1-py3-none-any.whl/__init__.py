import inspect
import os
import sys

__version__ = '0.2.1'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
sys.path.append(real_path)

try:
    from MCServerLib import Setup
except ImportError as e:
    print(e, " 추가할 수 없습니다.")
    exit(1)


__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]

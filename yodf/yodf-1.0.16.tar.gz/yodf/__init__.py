__version__ = '1.0.0'

# If you want exports from a module to be available as
# yod.export_name then do 'import *' for that module
# With below imports
#   - yod.core.Variable, yod.operations.constant can also be used
#     in the code as yod.Variable and yod.constant respectively
#   - exports from train on the other hand will have to be used
#     in the code as yod.train.GradientDescentOptimizer
from .core import *
from .operations import *
from . import train

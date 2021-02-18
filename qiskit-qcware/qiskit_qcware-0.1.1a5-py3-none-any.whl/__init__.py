"""
This is a qiskit provider for the QC Ware "Forge" product,
allowing evaluation of circuits on a local simulator or 
our hosted GPU-accelerated quantum simulators
"""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)


from .qcware_job import QcwareJob
from .qcware_provider import QcwareProvider

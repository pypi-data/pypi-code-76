__version__ = "1.0.2"

__all__ = ["FileServiceClient"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .file_service_client import FileServiceClient
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover

"""Version."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore[no-redef]

try:
    __version__ = importlib_metadata.version("python-grace")
except importlib_metadata.PackageNotFoundError:
    # Undefined during installation (build.py).
    __version__ = None  # type: ignore[assignment]

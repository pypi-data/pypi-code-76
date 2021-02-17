__version__ = "1.1.3"

__all__ = ["AnalyticDatasetClient",
           "AnalyticDatasetModel",
           "AnalyticDatasetDefinitionClient",
           "AnalyticDatasetDefinitionModel",
           "Granularity",
           "AnalyticDatasetFormat"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .analytic_dataset_client import AnalyticDatasetClient
    from .analytic_dataset_definition_client import AnalyticDatasetDefinitionClient
    from .models import AnalyticDatasetModel, AnalyticDatasetDefinitionModel, Granularity, AnalyticDatasetFormat
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover

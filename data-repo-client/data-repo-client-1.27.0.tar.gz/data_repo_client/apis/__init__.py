
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.data_repository_service_api import DataRepositoryServiceApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from data_repo_client.api.data_repository_service_api import DataRepositoryServiceApi
from data_repo_client.api.repository_api import RepositoryApi
from data_repo_client.api.resources_api import ResourcesApi
from data_repo_client.api.unauthenticated_api import UnauthenticatedApi

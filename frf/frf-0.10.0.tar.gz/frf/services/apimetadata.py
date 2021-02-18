"""Declares :class:`APIMetadataService`."""
from typing import List


class APIMetadataService:
    """Provides an interface to query the API metadata."""

    async def get(self, asgi, request):
        """Return a dictionary holding all API properties."""
        return {
            'capabilities': await self.capabilities(asgi, request),
            'catalog': await self.catalog(asgi, request)
        }

    async def catalog(self, asgi, request) -> dict:
        """Construct the API catalog."""
        return {
            'version': 'v1',
            'endpoints': {x.name: request.url_for(x.name) for x in asgi.routes}
        }

    async def capabilities(self, asgi, request) -> List[str]:
        """Return the list of API capabilities."""
        return []

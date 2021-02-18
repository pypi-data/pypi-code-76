"""Declares :class:`ServiceMetadataResource`."""
from fastapi import Request

from ..dependency import Injected
from ..views import AnonymousResource


class ServiceMetadataResource(AnonymousResource):
    resource_name = "Metadata"

    async def list(self, request: Request, svc=Injected('APIMetadataService')):
        """Return a JSON object describing all API properties."""
        return await svc.get(self.asgi, request)
